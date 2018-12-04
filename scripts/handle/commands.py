#  -*- encoding: utf-8 -*-

from os import sys, path

import psycopg2
import telegram

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.aes_cipher import AESCipher
from scripts.common.constants_and_variables import BotVariables, BotConstants
from scripts.commands.stats.stats_main import StatsMain


class HandleCommands(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.aes_cipher = AESCipher(self.bot_variables.crypt_key_length, self.bot_variables.crypt_key)

    def get_athlete_token(self, bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        username = update.message.from_user.username
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_FETCH_TOKEN.format(telegram_username=username))
        result = cursor.fetchone()
        cursor.close()
        database_connection.close()
        if result:
            return self.aes_cipher.decrypt(result[0])
        else:
            return False

    def main(self):
        athlete_token = self.get_athlete_token(self.bot, self.update)
        if athlete_token:
            command = self.update.message.text

            if command == "/start":
                message = self.bot_constants.MESSAGE_START_COMMAND.format(
                    first_name=self.update.message.from_user.first_name)
                self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

            elif command == "/stats":
                message = self.bot_constants.MESSAGE_STATS_COMMAND.format(
                    first_name=self.update.message.from_user.first_name)
                self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
                stats = StatsMain(self.bot, self.update, self.user_data, athlete_token)
                stats.process()

        else:
            message = self.bot_constants.MESSAGE_UNREGISTERED_ATHLETE.format(
                first_name=self.update.message.from_user.first_name,
                registration_url=self.bot_variables.registration_url,
                admin_user_name=self.aes_cipher.decrypt(self.bot_variables.admin_user_name))
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
