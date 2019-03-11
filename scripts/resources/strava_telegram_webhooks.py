#  -*- encoding: utf-8 -*-

import json
import logging
import traceback

import requests

from common.constants_and_variables import BotVariables, BotConstants


class StravaTelegramWebhooksResource(object):

    def __init__(self):
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.host = self.bot_variables.api_host

    def token_exchange(self, code):
        result = {}
        endpoint = self.bot_constants.API_TOKEN_EXCHANGE.format(host=self.host, code=code)
        try:
            logging.info("Requesting token exchange..")
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = response.json()

        return result if result != {} else False

    def athlete_exists(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_ATHLETE_EXISTS.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Checking if athlete {athlete_id} already exists..".format(athlete_id=athlete_id))
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    def update_stats(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_UPDATE_STATS.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Sending request to update stats for {athlete_id}".format(athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    def update_all_stats(self):
        result = False
        endpoint = self.bot_constants.API_UPDATE_ALL_STATS.format(host=self.host)
        try:
            logging.info("Sending request to update stats for all the registered athletes")
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    def database_write(self, query):
        result = False
        endpoint = self.bot_constants.API_DATABASE_WRITE.format(host=self.host)
        data = json.dumps({"query": query})
        try:
            logging.info("Requesting write operation to the database..")
            response = requests.post(endpoint, data=data, headers={"Content-Type": "application/json"})
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    def database_read_all(self, query):
        result = False
        endpoint = self.bot_constants.API_DATABASE_READ_ALL.format(host=self.host)
        data = json.dumps({"query": query})
        try:
            logging.info("Requesting read all operation to the database..")
            response = requests.get(endpoint, data=data, headers={"Content-Type": "application/json"})
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = response.json()

        return result

    def shadow_message(self, message):
        result = False
        endpoint = self.bot_constants.API_SHADOW_MESSAGE.format(host=self.host)
        data = json.dumps({"message": message})
        try:
            logging.info("Requesting to send shadow message..")
            response = requests.post(endpoint, data=data, headers={"Content-Type": "application/json"})
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    def get_athlete_id(self, telegram_username):
        athlete_id = False
        endpoint = self.bot_constants.API_GET_ATHLETE_ID.format(host=self.host, telegram_username=telegram_username)
        try:
            logging.info("Requesting Athlete ID..")
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                athlete_id = response.json()

        return athlete_id

    def get_gear_name(self, token, gear_id):
        gear_name = False
        endpoint = self.bot_constants.API_GET_GEAR_NAME.format(host=self.host, token=token, gear_id=gear_id)
        try:
            logging.info("Requesting gear name..")
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                gear_name = response.json()

        return gear_name

    def get_athlete(self, athlete_id):
        token = False
        endpoint = self.bot_constants.API_GET_ATHLETE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Requesting athlete {athlete_id}..".format(athlete_id=athlete_id))
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                token = response.json()

        return token

    def get_athlete_info(self, token):
        athlete_info = False
        endpoint = self.bot_constants.API_GET_STRAVA_ATHLETE_INFO.format(host=self.host, token=token)
        try:
            logging.info("Requesting athlete info from Strava..")
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                athlete_info = response.json()

        return athlete_info

    def get_athlete_by_telegram_username(self, telegram_username):
        token = False
        endpoint = self.bot_constants.API_GET_ATHLETE_BY_TELEGRAM_USERNAME.format(host=self.host,
                                                                                  telegram_username=telegram_username)
        try:
            logging.info("Requesting athlete {telegram_username}..".format(telegram_username=telegram_username))
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                token = response.json()

        return token

    def get_athlete_stats(self, telegram_username):
        stats = False
        endpoint = self.bot_constants.API_GET_STATS.format(host=self.host, telegram_username=telegram_username)
        try:
            logging.info("Requesting stats for {telegram_username}..".format(telegram_username=telegram_username))
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                stats = response.json()

        return stats
