# stdlib
from os import environ as env

# third-party

# local
import load_env


class Config():
    """
    Class to hold environment variables for the collector module
    """
    settings = {}

    def __init__(self):
        try:
            self.settings['reddit_secret'] = env['REDDIT_SECRET']
            self.settings['reddit_id'] = env['REDDIT_ID']
        except KeyError as e:
            raise Exception(e)

    @property
    def reddit_secret(self):
        return self.settings['reddit_secret']

    @property
    def reddit_id(self):
        return self.settings['reddit_id']
