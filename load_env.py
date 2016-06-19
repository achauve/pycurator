import logging
import os
import os.path as osp


def read_env():
    """
    Try to load your config stored in '.env' file.
    Useful for customizing dev options.
    """
    config = {}
    try:
        this_directory = osp.dirname(osp.realpath(__file__))
        env_file = osp.join(this_directory, '.env')
        with open(env_file) as env_file:
            for line in env_file:
                splits = line.strip().split('=')
                config[splits[0]] = '='.join(splits[1:])
    except:
        logging.info('could not load config from .env file')
    return config


# update env vars
os.environ.update(read_env())
