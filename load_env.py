import logging
import os
import os.path as osp
from typing import Dict


def read_env() -> Dict:
    """
    Try to load your config stored in '.env' file.
    Useful for customizing dev options.
    """
    config = {}
    try:
        this_directory = osp.dirname(osp.realpath(__file__))
        env_filename = osp.join(this_directory, '.env')
        with open(env_filename) as env_file:
            for line in env_file:
                splits = line.strip().split('=')
                config[splits[0]] = '='.join(splits[1:])
    except:
        logging.info('could not load config from .env file')
    return config


# update env vars
os.environ.update(read_env())
