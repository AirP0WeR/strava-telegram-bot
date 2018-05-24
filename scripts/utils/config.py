import json
import logging
import os


class Config(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def main():
        config_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(config_path, 'config.json')
        with open(config_file, 'r') as f:
            config = json.load(f)

        return config
