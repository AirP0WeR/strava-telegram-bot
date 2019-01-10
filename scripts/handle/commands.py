#  -*- encoding: utf-8 -*-

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
        self.athlete_id = None

    def get_athlete_id(self, telegram_username):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_GET_ATHLETE_ID.format(telegram_username=telegram_username))
        athlete_id = cursor.fetchone()
        cursor.close()
        database_connection.close()
        if athlete_id:
            return athlete_id[0]
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
        stats = ProcessStats(self.bot, self.update, self.user_data, self.athlete_id)
        stats.process()

    def refresh_command(self):
        message = "Failed to update stats."
        response = requests.post(self.bot_constants.API_WEBHOOK_UPDATE_STATS.format(athlete_id=self.athlete_id))
        if response.status_code == 200:
            message = "Refreshing.. Check stats after a minute."
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

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
                '/refresh': self.refresh_command
            })

            options[command]()

        else:
            message = self.bot_constants.MESSAGE_UNREGISTERED_ATHLETE.format(
                first_name=self.update.message.from_user.first_name,
                registration_url=self.bot_variables.registration_url,
                admin_user_name=self.bot_variables.admin_user_name)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
