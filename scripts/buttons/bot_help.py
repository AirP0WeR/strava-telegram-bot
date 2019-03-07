#  -*- encoding: utf-8 -*-

from collections import defaultdict

from clients.database import DatabaseClient
from common.constants_and_variables import BotConstants, BotVariables
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class BotHelp(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_constants = BotConstants()
        self.bot_variables = BotVariables()
        self.query = self.update.callback_query
        self.chosen_option = self.query.data
        self.chat_id = self.query.message.chat_id
        self.message_id = self.query.message.message_id
        self.telegram_username = self.query.message.chat.username
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()
        self.database_client = DatabaseClient()

    def help_exit_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_HELP_EXIT
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def help_registration_button(self):
        message = self.bot_constants.MESSAGE_HELP_REGISTRATION_DEVICE
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_HELP_REGISTRATION)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def help_commands_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_HELP_COMMANDS
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def help_registration_ios_button(self):
        self.user_data.clear()
        photo_path = 'scripts/commands/help/username/ios.jpeg'
        caption = "Note down you Telegram username (Telegram -> Settings -> Click on your profile -> Username). Enter this after authorizing the bot using the URL: {registration_url}".format(
            registration_url=self.bot_variables.registration_url)
        self.bot.send_photo(chat_id=self.chat_id, photo=open(photo_path, 'rb'), caption=caption)
        self.bot.send_photo(chat_id=self.bot_variables.shadow_mode_chat_id, photo=open(photo_path, 'rb'),
                            caption=caption)

    def help_registration_android_button(self):
        self.user_data.clear()
        photo_path = 'scripts/commands/help/username/android.jpeg'
        caption = "Note down you Telegram username (Telegram -> Settings -> Username). Enter this after authorizing the bot using the URL: {registration_url}".format(
            registration_url=self.bot_variables.registration_url)
        self.bot.send_photo(chat_id=self.chat_id, photo=open(photo_path, 'rb'), caption=caption)
        self.bot.send_photo(chat_id=self.bot_variables.shadow_mode_chat_id, photo=open(photo_path, 'rb'),
                            caption=caption)

    def process(self):
        options = defaultdict(lambda: self.help_exit_button, {
            'help_registration': self.help_registration_button,
            'help_commands': self.help_commands_button,
            'help_registration_ios': self.help_registration_ios_button,
            'help_registration_android': self.help_registration_android_button,
            'help_exit': self.help_exit_button,
        })

        options[self.chosen_option]()
