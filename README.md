Pycurator
=========

Tweet to email curation tool. Send each tweet from your selected [private] Twitter lists as an email.


## Why Pycurator?

Twitter is great to keep current with startups and software development news. 
But existing twitter clients are bad at keeping track of what you’ve already read.
Email clients are good at that though! Why not mix Twitter and emails?

*Tips*
- Use a small number of twitter private lists to group accounts you follow by priority. For instance, I use list L1 for tweets I don't want to miss, and then L2 for less important tweets. Of course you can add as many lists as you want.
- Carefully select which twitter accounts you add in these lists to avoid being overwhelmed. I prefer following accounts that tweet only about a few subjects and are not used as a real-time facebook wall.


## Deploy on heroku

- First [create a new twitter app](https://apps.twitter.com/) and get your credentials. You need your:
  - Consumer Key
  - Consumer Secret
  - Access Token
  - Access Token Secret

- Then [![deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

- Finally configure the following environment variables using heroku UI (https://dashboard.heroku.com/apps/YOUR-APP/settings) or heroku cli command `heroku config set VAR_1=... VAR_2=...`:
  - your twitter credentials from step 1:
    - TWITTER_ACCESS_TOKEN
    - TWITTER_ACCESS_TOKEN_SECRET
    - TWITTER_CONSUMER_KEY
    - TWITTER_CONSUMER_SECRET
  - your twitter list names separated by a comma (e.g. for me: "L1,L2,HN")
    - TWITTER_LIST_SLUGS
  - your twitter screen name (e.g. @adrienchauve)
    - TWITTER_SCREEN_NAME
  - the configuration of your SMTP server:
    - SMTP_HOST   [= "smtp.sendgrid.net" if you use sendgrid]
    - SMTP_PORT   [= "587" for most cases, including sendgrid]
    - SMTP_USERNAME [= the value of SENGRID_USERNAME if you use heroku addon]
    - SMTP_PASSWORD [= the value of SENDGRID_PASSWORD if you use heroku addon]
  - your redis URL:
    - REDIS_URL  [= will be already filled if you use heroku-redis addon]
  - the email address you want to receive the emails on:
    - EMAIL_RECIPIENT
  - and finally if you want to run the script without actually sending you emails but instead just printing eveything to the console (and logentries if you added it as an heroku addon):
    - DRY_RUN=false
  
## Next

- Add Reddit as a curation source
