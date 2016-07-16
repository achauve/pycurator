pycurator
=========

Python script to fetch tweets from twitter lists and send them by email.


## Deploy on heroku

- First [Create a new twitter app](https://apps.twitter.com/) and get your credentials. You need your:
  - Consumer Key
  - Consumer Secret
  - Access Token
  - Access Token Secret

- Then [![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

- Or manually: [Create a new heroku app](https://dashboard.heroku.com/new) and then:
  - You need to add at least the free version of the heroku redis add-on.
  - [Optional] Add the logentries add-on to keep track of your logs.
  - Set the environment variables:
    - TWITTER_ACCESS_TOKEN
    - TWITTER_ACCESS_TOKEN_SECRET
    - TWITTER_CONSUMER_KEY
    - TWITTER_CONSUMER_SECRET
    - TWITTER_LIST_SLUGS
    - TWITTER_SCREEN_NAME
    - SMTP_HOST
    - SMTP_PORT
    - SMTP_USERNAME
    - SMTP_PASSWORD
  - Scale your app (add one worker):
  
    ```shell
    heroku scale workers=1
    ```
