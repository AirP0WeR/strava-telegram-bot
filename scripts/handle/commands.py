#  -*- encoding: utf-8 -*-

import logging
import time
from collections import defaultdict
from os import sys, path

import requests
import telegram

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.constants_and_variables import BotVariables, BotConstants
from scripts.commands.stats.process import ProcessStats
from scripts.clients.database import DatabaseClient


class HandleCommands(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.database_client = DatabaseClient()
        self.athlete_id = None

    def get_athlete_id(self, telegram_username):
        athlete_id = self.database_client.read_operation(
            self.bot_constants.QUERY_GET_ATHLETE_ID.format(telegram_username=telegram_username))
        if athlete_id:
            return athlete_id[0]
        else:
            return None

    def get_athlete_token(self, athlete_id):
        result = self.database_client.read_operation(self.bot_constants.QUERY_FETCH_TOKEN.format(athlete_id=athlete_id))
        if len(result) > 0:
            access_token = result[0]
            refresh_token = result[1]
            expires_at = result[2]
            current_time = int(time.time())
            if current_time > expires_at:
                logging.info(
                    "Token has expired | Current Time: {current_time} | Token Expiry Time: {expires_at}".format(
                        current_time=current_time, expires_at=expires_at))
                access_token = self.refresh_and_update_token(athlete_id, refresh_token)
                return access_token
            else:
                logging.info(
                    "Token is still valid | Current Time: {current_time} | Token Expiry Time: {expires_at}".format(
                        current_time=current_time, expires_at=expires_at))
                return access_token
        else:
            return False

    def refresh_and_update_token(self, athlete_id, refresh_token):
        response = requests.post(self.bot_constants.API_TOKEN_EXCHANGE, data={
            'client_id': int(self.bot_variables.client_id),
            'client_secret': self.bot_variables.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }).json()

        access_info = dict()
        access_info['access_token'] = response['access_token']
        access_info['refresh_token'] = response['refresh_token']
        access_info['expires_at'] = response['expires_at']

        self.database_client.write_operation(self.bot_constants.QUERY_UPDATE_TOKEN.format(
            access_token=access_info['access_token'],
            refresh_token=access_info['refresh_token'],
            expires_at=access_info['expires_at'],
            athlete_id=athlete_id
        ))

        return response['access_token']

    def start_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_START_COMMAND.format(
            first_name=self.update.message.from_user.first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    def stats_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_STATS_COMMAND.format(
            first_name=self.update.message.from_user.first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        stats = ProcessStats(self.bot, self.update, self.user_data, self.athlete_id)
        stats.process()

    def refresh_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_STATS_FAILED
        response = requests.post(self.bot_constants.API_WEBHOOK_UPDATE_STATS.format(athlete_id=self.athlete_id))
        if response.status_code == 200:
            message = self.bot_constants.MESSAGE_UPDATE_STATS_STARTED
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    def auto_update_indoor_ride_command(self):
        self.user_data.clear()
        athlete_token = self.get_athlete_token(self.athlete_id)
        self.user_data['auto_update_indoor_ride'] = {'athlete_id': self.athlete_id, 'athlete_token': athlete_token}

        update_indoor_ride = self.database_client.read_operation(
            self.bot_constants.QUERY_FETCH_UPDATE_INDOOR_RIDE.format(athlete_id=self.athlete_id))
        if update_indoor_ride[0]:
            self.update.message.reply_text(self.bot_constants.MESSAGE_SHOULD_UPDATE_INDOOR_RIDE_DISABLE,
                                           reply_markup=self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_DISABLE_PROMPT)
        else:
            self.update.message.reply_text(self.bot_constants.MESSAGE_UPDATE_INDOOR_RIDE_CHOOSE_ACTIVITY_NAME,
                                           reply_markup=self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_NAME)

    def refresh_all_stats_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_STATS_FAILED
        response = requests.post(self.bot_constants.API_WEBHOOK_UPDATE_STATS_ALL)
        if response.status_code == 200:
            message = self.bot_constants.MESSAGE_UPDATE_STATS_STARTED_ALL
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    def cancel_command(self):
        self.user_data.clear()
        self.update.message.reply_text(self.bot_constants.MESSAGE_CANCEL_CURRENT_OPERATION)

    def process(self):
        self.bot.send_chat_action(chat_id=self.update.message.chat_id, action=telegram.ChatAction.TYPING)
        telegram_username = self.update.message.from_user.username
        self.athlete_id = self.get_athlete_id(telegram_username)
        if self.athlete_id:
            command = self.update.message.text
            self.bot.send_chat_action(chat_id=self.update.message.chat_id, action=telegram.ChatAction.TYPING)

            options = defaultdict(lambda: self.start_command, {
                '/start': self.start_command,
                '/stats': self.stats_command,
                '/refresh_stats': self.refresh_command,
                '/auto_update_indoor_ride': self.auto_update_indoor_ride_command,
                '/cancel': self.cancel_command,
                '/refresh_all_stats': self.refresh_all_stats_command
            })

            options[command]()

        else:
            message = self.bot_constants.MESSAGE_UNREGISTERED_ATHLETE.format(
                first_name=self.update.message.from_user.first_name,
                registration_url=self.bot_variables.registration_url,
                admin_user_name=self.bot_variables.admin_user_name)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
