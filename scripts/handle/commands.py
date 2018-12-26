#  -*- encoding: utf-8 -*-

import time
from collections import defaultdict
from os import sys, path

import psycopg2
import telegram

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.aes_cipher import AESCipher
from scripts.common.constants_and_variables import BotVariables, BotConstants
from scripts.commands.stats.calculate import CalculateStats
from scripts.clients.strava import StravaClient


class HandleCommands(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.aes_cipher = AESCipher(self.bot_variables.crypt_key_length, self.bot_variables.crypt_key)
        self.athlete_token = None

    def refresh_and_update_token(self, telegram_username, refresh_token):
        strava_client = StravaClient().get_client()
        access_info = strava_client.refresh_access_token(
            client_id=int(self.aes_cipher.decrypt(self.bot_variables.client_id)),
            client_secret=self.aes_cipher.decrypt(self.bot_variables.client_secret),
            refresh_token=refresh_token
        )

        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_UPDATE_TOKEN.format(
            access_token=self.aes_cipher.encrypt(access_info['access_token']),
            refresh_token=self.aes_cipher.encrypt(access_info['refresh_token']),
            expires_at=access_info['expires_at'],
            telegram_username=telegram_username
        ))
        cursor.close()
        database_connection.commit()
        database_connection.close()

        return access_info['access_token']

    def get_athlete_token(self, telegram_username):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_FETCH_TOKEN.format(telegram_username=telegram_username))
        result = cursor.fetchall()
        cursor.close()
        database_connection.close()
        if result:
            access_token = self.aes_cipher.decrypt(result[0][0])
            refresh_token = self.aes_cipher.decrypt(result[0][1])
            expires_at = result[0][2]
            if expires_at > int(time.time()):
                return access_token
            else:
                access_token = self.refresh_and_update_token(telegram_username, refresh_token)
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
        stats = CalculateStats(self.bot, self.update, self.user_data, self.athlete_token)
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
                admin_user_name=self.aes_cipher.decrypt(self.bot_variables.admin_user_name))
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
