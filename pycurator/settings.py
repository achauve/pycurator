import os
from logging.config import dictConfig
from typing import Optional

from . import load_env  # noqa


def env_var(key: str, default: str=None) -> Optional[str]:
    val = os.environ.get(key)
    if val is None:
        return default
    return val


def required_env_var(key: str) -> str:
    val = env_var(key)
    if val is None:
        raise Exception('Environment variable "%s" is not defined' % key)
    return val


def bool_env_var(key: str, default: bool=None) -> Optional[bool]:
    val = env_var(key)
    if val is None:
        return default

    if val.lower() == 'true':
        return True
    elif val.lower() == 'false':
        return False

    raise Exception('Environment variable "%s" should be either "true" or "false"' % key)


class Settings:
    TWITTER_ACCESS_TOKEN = required_env_var('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = required_env_var('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_CONSUMER_KEY = required_env_var('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = required_env_var('TWITTER_CONSUMER_SECRET')
    TWITTER_LIST_SLUGS = required_env_var('TWITTER_LIST_SLUGS')
    TWITTER_SCREEN_NAME = required_env_var('TWITTER_SCREEN_NAME')

    SMTP_USERNAME = required_env_var('SMTP_USERNAME')
    SMTP_PASSWORD = required_env_var('SMTP_PASSWORD')
    SMTP_HOST = required_env_var('SMTP_HOST')
    SMTP_PORT = required_env_var('SMTP_PORT')

    EMAIL_RECIPIENT = required_env_var('EMAIL_RECIPIENT')

    REDIS_URL = env_var('REDIS_URL', 'redis://localhost:6379')

    DRY_RUN = bool_env_var('DRY_RUN', True)
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
