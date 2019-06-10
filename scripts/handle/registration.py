#  -*- encoding: utf-8 -*-

from common.constants_and_variables import BotVariables, BotConstants
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class HandleRegistration:

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_variables = BotVariables()
        self.bot_constants = BotConstants()
        self.telegram_user_first_name = self.update.message.from_user.first_name
        self.telegram_username = self.update.message.from_user.username
        self.command = self.update.message.text
        self.chat_id = update.message.chat_id
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()

    def next_command(self):
        if self.telegram_username:
            message = "I see that your Telegram username is: `{telegram_username}`\n\nFollow the below steps to signup:".format(
                telegram_username=self.telegram_username)
            self.strava_telegram_webhooks_resource.shadow_message(message)
            self.auth_and_reg()
        else:
            message = "Looks like you haven't set your Telegram username yet. Follow the above steps and click /next to continue or message {admin_user_name} for additional help.".format(
                admin_user_name=self.bot_variables.admin_user_name)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)

    def auth_and_reg(self):
        photo_path = "scripts/commands/help/registration/strava_app_auth.PNG"
        caption = "Open the following link and login to your Strava account and click on Authorize.\n\n{registration_url}".format(
            registration_url=self.bot_variables.registration_url)
        self.bot.send_photo(chat_id=self.chat_id, photo=open(photo_path, 'rb'), caption=caption)
        photo_path = "scripts/commands/help/registration/telegram_reg.png"
        caption = "Once you Authorize, enter your Telegram username:\n\n{telegram_username}\n\nand click on Submit.\n\nOnce done, come back to this chat and click /next to continue.".format(
            telegram_username=self.telegram_username)
        self.bot.send_photo(chat_id=self.chat_id, photo=open(photo_path, 'rb'), caption=caption)
        self.strava_telegram_webhooks_resource.shadow_message(
            "Sent Authorize and Registration screenshots to the user.")

    def registration(self):
        message = "Hi {first_name}, Welcome to Cadence90 Bot! I will help you out in signing up for the bot.\n\n".format(
            first_name=self.telegram_user_first_name)
        if self.telegram_username:
            message += "I see that your Telegram username is: `{telegram_username}`\n\nFollow the below steps to signup:".format(
                telegram_username=self.telegram_username)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
            self.auth_and_reg()
        else:
            message += "You haven't set your username in Telegram yet which is required to signup for the bot. Let me show you how. Choose the type of device you are using:"
            self.update.message.reply_text(message, disable_web_page_preview=True,
                                           reply_markup=self.bot_constants.KEYBOARD_HELP_REGISTRATION)
            self.strava_telegram_webhooks_resource.shadow_message(message)

    def main(self):
        if self.command == "/next":
            self.next_command()
        else:
            self.registration()
