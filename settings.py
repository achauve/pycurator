from logging.config import dictConfig

import load_env  # noqa

from os import getenv


def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements
    """
    val = getenv(key, default)
    if isinstance(val, str) and val.lower() == 'true':
        return True
    elif isinstance(val, str) and val.lower() == 'false':
        return False
    return val


class Settings:
    TWITTER_ACCESS_TOKEN = env_var('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = env_var('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_CONSUMER_KEY = env_var('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = env_var('TWITTER_CONSUMER_SECRET')
    TWITTER_LIST_SLUGS = env_var('TWITTER_LIST_SLUGS')
    TWITTER_SCREEN_NAME = env_var('TWITTER_SCREEN_NAME')

    SMTP_USERNAME = env_var('SMTP_USERNAME')
    SMTP_PASSWORD = env_var('SMTP_PASSWORD')
    SMTP_HOST = env_var('SMTP_HOST')
    SMTP_PORT = env_var('SMTP_PORT')

    EMAIL_RECIPIENT = env_var('EMAIL_RECIPIENT')

    REDIS_URL = env_var('REDIS_URL', 'redis://localhost:6379')

    DRY_RUN = env_var('DRY_RUN', True)
    LOG_LEVEL = env_var('LOG_LEVEL', 'INFO')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] [%(pathname)s:%(lineno)d] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': Settings.LOG_LEVEL,
    },
}
dictConfig(LOGGING)
