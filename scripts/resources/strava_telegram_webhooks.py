#  -*- encoding: utf-8 -*-

import logging
import traceback

import requests
import ujson

from common.constants_and_variables import BotVariables, BotConstants
from common.execution_time import execution_time


class StravaTelegramWebhooksResource:

    def __init__(self):
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.host = self.bot_variables.api_host

    @execution_time
    def athlete_exists(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_ATHLETE_EXISTS.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Checking if athlete %s already exists..", athlete_id)
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                result = True

        return result

    @execution_time
    def update_stats(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_UPDATE_STATS.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Sending request to update stats for %s", athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                result = True

        return result

    @execution_time
    def update_challenges_stats(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_UPDATE_CHALLENGES_STATS.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Sending request to update challenges stats for %s", athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                result = True

        return result

    @execution_time
    def approve_payment_for_challenge(self, column_name, athlete_id):
        result = False
        endpoint = self.bot_constants.API_APPROVE_PAYMENT.format(host=self.host, column_name=column_name,
                                                                 athlete_id=athlete_id)
        try:
            logging.info("Sending request to approve payment for %s in %s", athlete_id, column_name)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                result = response.json()

        return result

    @execution_time
    def send_message(self, message):
        result = False
        endpoint = self.bot_constants.API_SEND_MESSAGE.format(host=self.host)
        data = ujson.dumps({"message": message})
        try:
            logging.info("Requesting to send Telegram message..")
            response = requests.post(endpoint, data=data, headers={"Content-Type": "application/json"})
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                bikes = response.json()

        return bikes

    @execution_time
    def get_athlete(self, athlete_id):
        token = False
        endpoint = self.bot_constants.API_GET_ATHLETE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Requesting athlete %s..", athlete_id)
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                token = response.json()

        return token

    @execution_time
    def get_athlete_by_telegram_username(self, telegram_username):
        token = False
        endpoint = self.bot_constants.API_GET_ATHLETE_BY_TELEGRAM_USERNAME.format(host=self.host,
                                                                                  telegram_username=telegram_username)
        try:
            logging.info("Requesting athlete %s..", telegram_username)
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                token = response.json()

        return token

    @execution_time
    def get_athlete_stats(self, telegram_username):
        stats = False
        endpoint = self.bot_constants.API_GET_STATS.format(host=self.host, telegram_username=telegram_username)
        try:
            logging.info("Requesting stats for %s..", telegram_username)
            response = requests.get(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                stats = response.json()

        return stats

    @execution_time
    def enable_activity_summary(self, chat_id, athlete_id):
        enable = False
        endpoint = self.bot_constants.API_ENABLE_ACTIVITY_SUMMARY.format(host=self.host, chat_id=chat_id,
                                                                         athlete_id=athlete_id)
        try:
            logging.info("Request to enable activity summary for %s with chat id: %s", chat_id, athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                enable = True

        return enable

    @execution_time
    def disable_activity_summary(self, athlete_id):
        disable = False
        endpoint = self.bot_constants.API_DISABLE_ACTIVITY_SUMMARY.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to disable activity summary for %s", athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                disable = True

        return disable

    @execution_time
    def disable_auto_update_indoor_ride(self, athlete_id):
        disable = False
        endpoint = self.bot_constants.API_DISABLE_AUTO_UPDATE_INDOOR_RIDE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to disable auto update indoor ride for %s", athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                disable = True

        return disable

    @execution_time
    def update_chat_id(self, chat_id, athlete_id):
        update = False
        endpoint = self.bot_constants.API_UPDATE_CHAT_ID.format(host=self.host, chat_id=chat_id, athlete_id=athlete_id)
        try:
            logging.info(
                "Request to update chat id for for %s with chat id: %s", chat_id, athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                update = True

        return update

    @execution_time
    def activate_flag_athlete(self, athlete_id):
        activate = False
        endpoint = self.bot_constants.API_ACTIVATE_ATHLETE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to activate athlete %s", athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                activate = True

        return activate

    @execution_time
    def deactivate_flag_athlete(self, athlete_id):
        deactivate = False
        endpoint = self.bot_constants.API_DEACTIVATE_ATHLETE.format(host=self.host, athlete_id=athlete_id)
        try:
            logging.info("Request to deactivate athlete %s", athlete_id)
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
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
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                result = True

        return result

    @execution_time
    def challenges_deauth_athlete(self, athlete_id):
        result = False
        endpoint = self.bot_constants.API_DEAUTH_FROM_CHALLENGES.format(host=self.host,
                                                                        athlete_id=athlete_id)
        try:
            logging.info("Requesting to deauth athlete from challenges..")
            response = requests.post(endpoint)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("Response status code: %s", response.status_code)
            if response.status_code == 200:
                result = True

        return result
