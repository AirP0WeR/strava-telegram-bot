#  -*- encoding: utf-8 -*-

from common.constants_and_variables import BotConstants
from common.shadow_mode import ShadowMode


class ProcessStats(object):

    def __init__(self, update, bot):
        self.update = update
        self.bot = bot
        self.bot_constants = BotConstants()
        self.shadow_mode = ShadowMode(bot)

    def process(self):
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.update.message.reply_text(message, reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)
        self.shadow_mode.send_message(message=message)
