#  -*- encoding: utf-8 -*-

import logging
import traceback

import requests
import ujson

from common.constants_and_variables import BotVariables, BotConstants
from common.execution_time import execution_time


class StravaTelegramWebhooksResource(object):

    def __init__(self):
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.host = self.bot_variables.api_host

    @execution_time
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

    @execution_time
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

    @execution_time
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

    @execution_time
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

    @execution_time
    def update_challenges_stats(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_UPDATE_CHALLENGES_STATS.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Sending request to update challenges stats for {athlete_id}".format(athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    @execution_time
    def update_challenges_all_stats(self):
        result = False
        endpoint = self.bot_constants.API_UPDATE_CHALLENGES_ALL_STATS.format(host=self.host)
        try:
            logging.info("Sending request to update challenges stats for all the registered athletes")
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    @execution_time
    def database_write(self, query):
        result = False
        endpoint = self.bot_constants.API_DATABASE_WRITE.format(host=self.host)
        data = ujson.dumps({"query": query})
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

    @execution_time
    def database_read_all(self, query):
        result = False
        endpoint = self.bot_constants.API_DATABASE_READ_ALL.format(host=self.host)
        data = ujson.dumps({"query": query})
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

    @execution_time
    def shadow_message(self, message):
        result = False
        endpoint = self.bot_constants.API_SHADOW_MESSAGE.format(host=self.host)
        data = ujson.dumps({"message": message})
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

    @execution_time
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

    @execution_time
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

    @execution_time
    def get_bikes_list(self, token):
        bikes = False
        endpoint = self.bot_constants.API_GET_BIKES_LIST.format(host=self.host, token=token)
        try:
            logging.info("Requesting bikes list..")
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                bikes = response.json()

        return bikes

    @execution_time
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

    @execution_time
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

    @execution_time
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

    @execution_time
    def enable_activity_summary(self, chat_id, athlete_id):
        enable = False
        endpoint = self.bot_constants.API_ENABLE_ACTIVITY_SUMMARY.format(host=self.host, chat_id=chat_id,
                                                                         athlete_id=athlete_id)
        try:
            logging.info(
                "Request to enable activity summary for {athlete_id} with chat id: {chat_id}".format(chat_id=chat_id,
                                                                                                     athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                enable = True

        return enable

    @execution_time
    def disable_activity_summary(self, athlete_id):
        disable = False
        endpoint = self.bot_constants.API_DISABLE_ACTIVITY_SUMMARY.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to disable activity summary for {athlete_id}".format(athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                disable = True

        return disable

    @execution_time
    def disable_auto_update_indoor_ride(self, athlete_id):
        disable = False
        endpoint = self.bot_constants.API_DISABLE_AUTO_UPDATE_INDOOR_RIDE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to disable auto update indoor ride for {athlete_id}".format(athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                disable = True

        return disable

    @execution_time
    def update_chat_id(self, chat_id, athlete_id):
        update = False
        endpoint = self.bot_constants.API_UPDATE_CHAT_ID.format(host=self.host, chat_id=chat_id, athlete_id=athlete_id)
        try:
            logging.info(
                "Request to update chat id for for {athlete_id} with chat id: {chat_id}".format(chat_id=chat_id,
                                                                                                athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                update = True

        return update

    @execution_time
    def activate_flag_athlete(self, athlete_id):
        activate = False
        endpoint = self.bot_constants.API_ACTIVATE_ATHLETE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to activate athlete {athlete_id}".format(athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                activate = True

        return activate

    @execution_time
    def deactivate_flag_athlete(self, athlete_id):
        deactivate = False
        endpoint = self.bot_constants.API_DEACTIVATE_ATHLETE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to deactivate athlete {athlete_id}".format(athlete_id=athlete_id))
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                deactivate = True

        return deactivate

    @execution_time
    def get_even_challenges_athletes(self):
        challenges_even_athletes = False
        endpoint = self.bot_constants.API_LIST_EVEN_CHALLENGES_ATHLETES.format(host=self.host)
        try:
            logging.info("Requesting list of registered athletes for even challenges..")
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                challenges_even_athletes = response.json()

        return challenges_even_athletes

    @execution_time
    def get_odd_challenges_athletes(self):
        challenges_odd_athletes = False
        endpoint = self.bot_constants.API_LIST_ODD_CHALLENGES_ATHLETES.format(host=self.host)
        try:
            logging.info("Requesting list of registered athletes for odd challenges..")
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                challenges_odd_athletes = response.json()

        return challenges_odd_athletes

    @execution_time
    def challenges_hits_reset(self):
        result = False
        endpoint = self.bot_constants.API_CHALLENGES_HITS_RESET.format(host=self.host)
        try:
            logging.info("Requesting to reset challenges page hits count..")
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result

    @execution_time
    def challenges_delete_athlete(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_DEAUTH_AND_DELETE_FROM_CHALLENGES.format(host=self.host,
                                                                                   athlete_id=athlete_id)
        try:
            logging.info("Requesting to deauth and delete athlete from challenges..")
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            if response.status_code == 200:
                result = True

        return result
