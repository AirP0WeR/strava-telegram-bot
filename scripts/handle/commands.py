#  -*- encoding: utf-8 -*-

import logging
import time
from collections import defaultdict
from os import sys, path

import psycopg2
import requests
import telegram

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.constants_and_variables import BotVariables, BotConstants
from scripts.commands.stats.process import ProcessStats


class HandleCommands(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.athlete_token = None

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

        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_UPDATE_TOKEN.format(
            access_token=access_info['access_token'],
            refresh_token=access_info['refresh_token'],
            expires_at=access_info['expires_at'],
            athlete_id=athlete_id
        ))
        cursor.close()
        database_connection.commit()
        database_connection.close()

        return response['access_token']

    def get_athlete_token(self, telegram_username):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_FETCH_TOKEN.format(telegram_username=telegram_username))
        result = cursor.fetchall()
        cursor.close()
        database_connection.close()
        if result:
            athlete_id = result[0][0]
            access_token = result[0][1]
            refresh_token = result[0][2]
            expires_at = result[0][3]
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
            return None

    def start_command(self):
        message = self.bot_constants.MESSAGE_START_COMMAND.format(
            first_name=self.update.message.from_user.first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    def stats_command(self):
        message = self.bot_constants.MESSAGE_STATS_COMMAND.format(
            first_name=self.update.message.from_user.first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        stats = ProcessStats(self.bot, self.update, self.user_data, self.athlete_token)
        stats.process()

    def process(self):
        self.bot.send_chat_action(chat_id=self.update.message.chat_id, action=telegram.ChatAction.TYPING)
        telegram_username = self.update.message.from_user.username
        self.athlete_token = self.get_athlete_token(telegram_username)
        if self.athlete_token:
            command = self.update.message.text
            self.bot.send_chat_action(chat_id=self.update.message.chat_id, action=telegram.ChatAction.TYPING)

            options = defaultdict(lambda: self.start_command, {
                '/start': self.start_command,
                '/stats': self.stats_command
            })

            options[command]()

        else:
            message = self.bot_constants.MESSAGE_UNREGISTERED_ATHLETE.format(
                first_name=self.update.message.from_user.first_name,
                registration_url=self.bot_variables.registration_url,
                admin_user_name=self.bot_variables.admin_user_name)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
