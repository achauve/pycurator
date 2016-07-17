import logging
import time

import schedule
import tweepy
import redis

from settings import Settings
from email_tools import send_email, smtp_server

LIST_SLUGS = Settings.TWITTER_LIST_SLUGS.split(',')

redis_client = redis.from_url(Settings.REDIS_URL)


def last_tweet_id_redis_key(list_slug):
    return 'r1:last_tweet_id:{list_slug}'.format(list_slug=list_slug)


def load_last_tweet_id(list_slug):
    last_id = redis_client.get(last_tweet_id_redis_key(list_slug))
    logging.info('loading last_tweet_id for list "%s": %s' % (list_slug, last_id))
    return last_id


def save_last_tweet_id(last_id, list_slug):
    if not Settings.DRY_RUN:
        redis_client.set(last_tweet_id_redis_key(list_slug), last_id)
    logging.info('saving last_tweet_id for list "%s": %s' % (list_slug, last_id))


def get_tweets(api, list_slug, last_tweet_id):
    return api.list_timeline(Settings.TWITTER_SCREEN_NAME, list_slug, since_id=last_tweet_id)


def get_user_from_tweet(tweet):
    return {
        'name': tweet.author.name,
        'screen_name': tweet.author.screen_name,
        'profile_image_url': tweet.author.profile_image_url
    }


TWEET_TEMPLATE = """
    <table>
    <td>
    <a href="{tweet_link}"><img src={img_src}/></a>
    </td>
    <td>
        <strong>{user_name}</strong>&nbsp;@{user_screen_name}
        {retweet}
        <br>
        <small>{date}</small>
    </td>
    </table>
    <p>{text}</p>
    <p>{expanded_urls}</p>
    <br>
    <p>{media}</p>
"""

RETWEET_TEMPLATE = """
    <br>
    <strong>RT</strong>&nbsp;@{rt_screen_name} {rt_name}
"""


def html_img(url):
    return '<img src="{url}"/>'.format(url=url)


def parse_tweet(tweet):
    text = tweet.text

    retweet_user = None
    if hasattr(tweet, 'retweeted_status'):
        retweeted_status = tweet.retweeted_status
        retweet_user = get_user_from_tweet(retweeted_status)
        text = retweeted_status.text

    id_str = tweet.id_str
    created_at = tweet.created_at

    expanded_urls = []
    if 'urls' in tweet.entities:
        expanded_urls = [url['expanded_url'] for url in tweet.entities['urls']]

    media_urls = []
    if 'media' in tweet.entities:
        media_urls = [html_img(media['media_url']) for media in tweet.entities['media']]

    user = get_user_from_tweet(tweet)

    return {
        'sender': Settings.SMTP_USERNAME,
        'msg_subject': '{name} -- {text}'.format(name=user['name'],
                                                 text=text.replace('\n', ' ')),
        'html_content': TWEET_TEMPLATE.format(
            img_src=user['profile_image_url'],
            tweet_link='https://twitter.com/{screen_name}/status/{tweet_id}'.format(
                screen_name=Settings.TWITTER_SCREEN_NAME,
                tweet_id=id_str),
            text=text,
            retweet=RETWEET_TEMPLATE.format(rt_screen_name=retweet_user['screen_name'],
                                            rt_name=retweet_user['name']) if retweet_user else '',
            user_name=user['name'],
            user_screen_name=user['screen_name'],
            date=created_at,
            expanded_urls='<br>'.join(expanded_urls),
            media='<br>'.join(media_urls))
    }


def fetch_tweets_and_send_emails():
    logging.info('-- starting fetching tweets and sending emails')

    auth = tweepy.OAuthHandler(Settings.TWITTER_CONSUMER_KEY, Settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(Settings.TWITTER_ACCESS_TOKEN, Settings.TWITTER_ACCESS_TOKEN_SECRET)

    twitter_api = tweepy.API(auth)

    with smtp_server() as server:

        for list_slug in LIST_SLUGS:

            last_tweet_id = load_last_tweet_id(list_slug)
            if last_tweet_id is None:
                logging.warning('no last tweet id was found for list %s' % list_slug)

            tweets = get_tweets(twitter_api, list_slug=list_slug, last_tweet_id=last_tweet_id)

            for tweet in reversed(tweets):
                kwargs = parse_tweet(tweet)
                kwargs['msg_subject'] = '[{list_slug}] {subject}'.format(list_slug=list_slug,
                                                                         subject=kwargs['msg_subject'])
                send_email(server, **kwargs)
                save_last_tweet_id(last_id=tweet.id_str, list_slug=list_slug)


def main():
    logging.info('starting pycurator')

    schedule.every(5).minutes.do(fetch_tweets_and_send_emails)

    fetch_tweets_and_send_emails()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
