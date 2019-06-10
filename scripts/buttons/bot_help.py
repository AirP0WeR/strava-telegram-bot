#  -*- encoding: utf-8 -*-

from collections import defaultdict

from common.constants_and_variables import BotConstants, BotVariables
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class BotHelp:

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

    def help_exit_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_HELP_EXIT
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.shadow_message(message)

    def help_registration_ios_button(self):
        self.user_data.clear()
        photo_path = 'scripts/commands/help/username/ios.jpeg'
        caption = "Go back to your Telegram's main screen -> Settings -> Click on your profile -> Username"
        self.bot.edit_message_text(text="Find the below screenshot:", chat_id=self.chat_id, message_id=self.message_id)
        self.bot.send_photo(chat_id=self.chat_id, photo=open(photo_path, 'rb'), caption=caption)
        message = "Once you set your Telegram username, come back to this chat and click /next to continue."
        self.bot.send_message(text=message, chat_id=self.chat_id, parse_mode="Markdown")
        self.strava_telegram_webhooks_resource.shadow_message("Sent iOS screenshot to the user.")

    def help_registration_android_button(self):
        self.user_data.clear()
        photo_path = 'scripts/commands/help/username/android.jpeg'
        caption = "Go back to your Telegram's main screen -> Settings -> Username"
        self.bot.edit_message_text(text="Find the below screenshot:", chat_id=self.chat_id, message_id=self.message_id)
        self.bot.send_photo(chat_id=self.chat_id, photo=open(photo_path, 'rb'), caption=caption)
        message = "Once you set your Telegram username, come back to this chat and click /next to continue."
        self.bot.send_message(text=message, chat_id=self.chat_id, parse_mode="Markdown")
        self.strava_telegram_webhooks_resource.shadow_message("Sent Android screenshot to the user.")

    def process(self):
        options = defaultdict(lambda: self.help_exit_button, {
            'help_registration_ios': self.help_registration_ios_button,
            'help_registration_android': self.help_registration_android_button,
            'help_exit': self.help_exit_button,
        })

        options[self.chosen_option]()
