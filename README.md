pycurator
=========

Python script to fetch tweets from twitter lists and send them by email.


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
  
