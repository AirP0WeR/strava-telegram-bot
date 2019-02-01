#  -*- encoding: utf-8 -*-

import time
from collections import defaultdict

import requests
import telegram

from clients.database import DatabaseClient
from clients.strava import StravaClient
from commands.stats.process import ProcessStats
from common.aes_cipher import AESCipher
from common.constants_and_variables import BotVariables, BotConstants
from common.shadow_mode import ShadowMode


class HandleCommands(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.database_client = DatabaseClient()
        self.strava_client = StravaClient()
        self.athlete_id = None
        self.telegram_user_first_name = self.update.message.from_user.first_name
        self.shadow_mode = ShadowMode(bot)
        self.aes_cipher = AESCipher(self.bot_variables.crypt_key_length, self.bot_variables.crypt_key)
        self.telegram_username = self.update.message.from_user.username
        self.chat_id = self.update.message.chat_id

    def get_athlete_id(self, telegram_username):
        athlete_id = self.database_client.read_operation(
            self.bot_constants.QUERY_GET_ATHLETE_ID.format(telegram_username=telegram_username))
        if athlete_id:
            return athlete_id[0]
        else:
            return None

    def get_athlete_token(self, athlete_id):
        access_token = None
        result = self.database_client.read_operation(self.bot_constants.QUERY_FETCH_TOKEN.format(athlete_id=athlete_id))
        if len(result) > 0:
            access_token = self.aes_cipher.decrypt(result[0])
            refresh_token = self.aes_cipher.decrypt(result[1])
            expires_at = result[2]

            if int(time.time()) > expires_at:
                access_token = self.refresh_and_update_token(athlete_id, refresh_token)

        return access_token

    def refresh_and_update_token(self, athlete_id, refresh_token):
        response = requests.post(self.bot_constants.API_TOKEN_EXCHANGE, data={
            'client_id': int(self.bot_variables.client_id),
            'client_secret': self.bot_variables.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }).json()

        self.database_client.write_operation(self.bot_constants.QUERY_UPDATE_TOKEN.format(
            access_token=self.aes_cipher.encrypt(response['access_token']),
            refresh_token=self.aes_cipher.encrypt(response['refresh_token']),
            expires_at=response['expires_at'],
            athlete_id=athlete_id
        ))

        return response['access_token']

    def start_command(self):
        self.user_data.clear()
        self.database_client.write_operation(self.bot_constants.QUERY_UPDATE_CHAT_ID.format(chat_id=self.chat_id,
                                                                                            athlete_id=self.athlete_id))
        message = self.bot_constants.MESSAGE_START_COMMAND.format(first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)

    def stats_command(self):
        self.user_data.clear()
        self.database_client.write_operation(self.bot_constants.QUERY_UPDATE_CHAT_ID.format(chat_id=self.chat_id,
                                                                                            athlete_id=self.athlete_id))
        stats = ProcessStats(self.update)
        stats.process()

    def refresh_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_STATS_FAILED.format(first_name=self.telegram_user_first_name)
        response = requests.post(self.bot_variables.api_update_stats_webhook.format(athlete_id=self.athlete_id))
        if response.status_code == 200:
            message = self.bot_constants.MESSAGE_UPDATE_STATS_STARTED.format(first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown",
                                       disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)

    def auto_update_indoor_ride_command(self):
        self.user_data.clear()
        athlete_token = self.get_athlete_token(self.athlete_id)
        self.user_data['auto_update_indoor_ride'] = {'athlete_id': self.athlete_id, 'athlete_token': athlete_token}

        update_indoor_ride = self.database_client.read_operation(
            self.bot_constants.QUERY_FETCH_UPDATE_INDOOR_RIDE.format(athlete_id=self.athlete_id))
        if update_indoor_ride[0]:
            configured_data = ""
            if update_indoor_ride[1]['name']:
                configured_data += "\nActivity Name: {activity_name}".format(
                    activity_name=update_indoor_ride[1]['name'])
            if update_indoor_ride[1]['gear_id']:
                strava_client = self.strava_client.get_client(athlete_token)
                bike_name = strava_client.get_gear(gear_id=update_indoor_ride[1]['gear_id']).name
                configured_data += "\nBike: {bike_name}".format(bike_name=bike_name)

            message = self.bot_constants.MESSAGE_SHOULD_UPDATE_INDOOR_RIDE_DISABLE.format(
                first_name=self.telegram_user_first_name, configuration=configured_data)
            reply_markup = self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_DISABLE_PROMPT
        else:
            message = self.bot_constants.MESSAGE_UPDATE_INDOOR_RIDE_CHOOSE_ACTIVITY_NAME.format(
                first_name=self.telegram_user_first_name)
            reply_markup = self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_NAME

        self.update.message.reply_text(message, reply_markup=reply_markup)
        self.shadow_mode.send_message(message=message)

    def refresh_all_stats_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_STATS_FAILED.format(first_name=self.telegram_user_first_name)
        response = requests.post(self.bot_variables.api_update_stats_all_webhook)
        if response.status_code == 200:
            message = self.bot_constants.MESSAGE_UPDATE_STATS_STARTED_ALL.format(
                first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown",
                                       disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)

    def all_athletes_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_FETCHING_REGISTERED_ATHLETES.format(
            first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        all_athletes = self.database_client.read_all_operation(self.bot_constants.QUERY_GET_ATHLETES)
        sl_no = 1
        names = "*List of registered athletes:*\n\n"
        for name in all_athletes:
            names += "{sl_no}. {name}\n".format(sl_no=sl_no, name=name[0])
            sl_no += 1

        self.update.message.reply_text(names, parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=names)

    def activity_summary_command(self):
        self.user_data.clear()
        self.user_data['ride_summary'] = {'athlete_id': self.athlete_id}
        enable_activity_summary = self.database_client.read_operation(
            self.bot_constants.QUERY_ACTIVITY_SUMMARY.format(athlete_id=self.athlete_id))
        if not enable_activity_summary[0]:
            message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_CONFIRMATION.format(
                first_name=self.telegram_user_first_name)
            reply_markup = self.bot_constants.KEYBOARD_ENABLE_ACTIVITY_SUMMARY_CONFIRMATION
        else:
            message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_SHOULD_DISABLE.format(
                first_name=self.telegram_user_first_name)
            reply_markup = self.bot_constants.KEYBOARD_ACTIVITY_SUMMARY_DISABLE_CONFIRMATION

        self.update.message.reply_text(message, reply_markup=reply_markup)
        self.shadow_mode.send_message(message=message)

    def help_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_HELP_TOPICS.format(first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, reply_markup=self.bot_constants.KEYBOARD_HELP_MENU)
        self.shadow_mode.send_message(message=message)

    def cancel_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_CANCEL_CURRENT_OPERATION
        self.update.message.reply_text(message)
        self.shadow_mode.send_message(message=message)

    def process(self):
        self.bot.send_chat_action(chat_id=self.chat_id, action=telegram.ChatAction.TYPING)
        self.athlete_id = self.get_athlete_id(self.telegram_username)
        if self.athlete_id:
            command = self.update.message.text
            self.bot.send_chat_action(chat_id=self.chat_id, action=telegram.ChatAction.TYPING)

            options = defaultdict(lambda: self.start_command, {
                '/start': self.start_command,
                '/stats': self.stats_command,
                '/refresh_stats': self.refresh_command,
                '/auto_update_indoor_ride': self.auto_update_indoor_ride_command,
                '/cancel': self.cancel_command,
                '/refresh_all_stats': self.refresh_all_stats_command,
                '/all_athletes': self.all_athletes_command,
                '/activity_summary': self.activity_summary_command,
                '/help': self.help_command
            })

            options[command]()

        else:
            message = self.bot_constants.MESSAGE_UNREGISTERED_ATHLETE.format(
                first_name=self.telegram_user_first_name,
                registration_url=self.bot_variables.registration_url,
                admin_user_name=self.bot_variables.admin_user_name)
            self.update.message.reply_text(message, disable_web_page_preview=True,
                                           reply_markup=self.bot_constants.KEYBOARD_HELP_MENU)
            self.shadow_mode.send_message(message=message, parse_mode=None)
