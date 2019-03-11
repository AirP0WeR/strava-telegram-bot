#  -*- encoding: utf-8 -*-

from collections import defaultdict

import telegram

from commands.stats.process import ProcessStats
from common.aes_cipher import AESCipher
from common.constants_and_variables import BotVariables, BotConstants
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class HandleCommands(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.telegram_user_first_name = self.update.message.from_user.first_name
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()
        self.aes_cipher = AESCipher(self.bot_variables.crypt_key_length, self.bot_variables.crypt_key)
        self.telegram_username = self.update.message.from_user.username
        self.chat_id = self.update.message.chat_id
        self.athlete_details = None

    def start_command(self):
        self.user_data.clear()
        self.strava_telegram_webhooks_resource.database_write(
            self.bot_constants.QUERY_UPDATE_CHAT_ID.format(chat_id=self.chat_id,
                                                           athlete_id=self.athlete_details['athlete_id']))
        message = self.bot_constants.MESSAGE_START_COMMAND.format(first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def stats_command(self):
        self.user_data.clear()
        self.strava_telegram_webhooks_resource.database_write(
            self.bot_constants.QUERY_UPDATE_CHAT_ID.format(chat_id=self.chat_id,
                                                           athlete_id=self.athlete_details['athlete_id']))
        stats = ProcessStats(self.update)
        stats.process()

    def refresh_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_STATS_FAILED.format(first_name=self.telegram_user_first_name)
        if self.strava_telegram_webhooks_resource.update_stats(self.athlete_details['athlete_id']):
            message = self.bot_constants.MESSAGE_UPDATE_STATS_STARTED.format(first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown",
                                       disable_web_page_preview=True)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def refresh_all_stats_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_STATS_FAILED.format(first_name=self.telegram_user_first_name)
        if self.strava_telegram_webhooks_resource.update_all_stats():
            message = self.bot_constants.MESSAGE_UPDATE_STATS_STARTED_ALL.format(
                first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown",
                                       disable_web_page_preview=True)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def all_athletes_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_FETCHING_REGISTERED_ATHLETES.format(
            first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        self.strava_telegram_webhooks_resource.shadow_message(message)
        all_athletes = self.strava_telegram_webhooks_resource.database_read_all(self.bot_constants.QUERY_GET_ATHLETES)
        sl_no = 0
        messages = list()
        names = "*List of registered athletes:*\n\n"
        for athlete in all_athletes:
            sl_no += 1
            names += "{sl_no}. [{name}](https://www.strava.com/athletes/{athlete_id})\n".format(sl_no=sl_no,
                                                                                                name=athlete[0],
                                                                                                athlete_id=athlete[1])
            if sl_no % 25 == 0:
                messages.append(names)
                names = "*List of registered athletes:*\n\n"
        messages.append(names)
        for name in messages:
            if name != "*List of registered athletes:*\n\n":
                self.update.message.reply_text(name, parse_mode="Markdown", disable_web_page_preview=True)
                self.strava_telegram_webhooks_resource.shadow_message(name)

    def activity_summary_command(self):
        self.user_data.clear()
        self.user_data['ride_summary'] = {'athlete_id': self.athlete_details['athlete_id']}
        if self.athlete_details['enable_activity_summary']:
            message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_SHOULD_DISABLE.format(
                first_name=self.telegram_user_first_name)
            reply_markup = self.bot_constants.KEYBOARD_ACTIVITY_SUMMARY_DISABLE_CONFIRMATION

        else:
            message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_CONFIRMATION.format(
                first_name=self.telegram_user_first_name)
            reply_markup = self.bot_constants.KEYBOARD_ENABLE_ACTIVITY_SUMMARY_CONFIRMATION

        self.update.message.reply_text(message, reply_markup=reply_markup)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def auto_update_indoor_ride_command(self):
        self.user_data.clear()
        self.user_data['auto_update_indoor_ride'] = {'athlete_id': self.athlete_details['athlete_id'],
                                                     'athlete_token': self.athlete_details['athlete_token']}
        if self.athlete_details['update_indoor_ride']:
            configured_data = ""
            if self.athlete_details['update_indoor_ride_data']['name']:
                configured_data += "\nActivity Name: {activity_name}".format(
                    activity_name=self.athlete_details['update_indoor_ride_data']['name'])
            if self.athlete_details['update_indoor_ride_data']['gear_id']:
                bike_name = self.strava_telegram_webhooks_resource.get_gear_name(self.athlete_details['athlete_token'],
                                                                                 self.athlete_details[
                                                                                     'update_indoor_ride_data'][
                                                                                     'gear_id'])
                configured_data += "\nBike: {bike_name}".format(bike_name=bike_name)

            message = self.bot_constants.MESSAGE_SHOULD_UPDATE_INDOOR_RIDE_DISABLE.format(
                first_name=self.telegram_user_first_name, configuration=configured_data)
            reply_markup = self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_DISABLE_PROMPT
        else:
            message = self.bot_constants.MESSAGE_UPDATE_INDOOR_RIDE_CHOOSE_ACTIVITY_NAME.format(
                first_name=self.telegram_user_first_name)
            reply_markup = self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_NAME

        self.update.message.reply_text(message, reply_markup=reply_markup)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def help_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_HELP_TOPICS.format(first_name=self.telegram_user_first_name)
        self.update.message.reply_text(message, reply_markup=self.bot_constants.KEYBOARD_HELP_MENU)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def cancel_command(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_CANCEL_CURRENT_OPERATION
        self.update.message.reply_text(message)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def process(self):
        self.bot.send_chat_action(chat_id=self.chat_id, action=telegram.ChatAction.TYPING)
        self.athlete_details = self.strava_telegram_webhooks_resource.get_athlete_by_telegram_username(
            self.telegram_username)
        if self.athlete_details:
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
            self.strava_telegram_webhooks_resource.shadow_message(
                "{first_name} tried using the bot, but is not registered yet.".format(
                    first_name=self.telegram_user_first_name))
