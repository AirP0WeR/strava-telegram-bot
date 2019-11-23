#  -*- encoding: utf-8 -*-

import logging
import traceback

import ujson

from scripts.clients.memcachier import MemcachierClient


class MemcachierResource:

    def __init__(self):
        self.memcachier_client = MemcachierClient().cache()

    def put_cache(self, key, value):
        result = False
        try:
            logging.info("Requesting put operation on cache. Key: %s | Value: %s", key, value)
            self.memcachier_client.set(key, value)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            result = True

        logging.info("Result: %s", result)
        return result

    def get_cache(self, key):
        result = False
        try:
            logging.info("Requesting get operation on cache. Key: %s", key)
            data = ujson.loads(self.memcachier_client.get(key))
        except Exception:
            logging.error(traceback.format_exc())
        else:
            result = data

        logging.info("Result: %s", result)
        return result
