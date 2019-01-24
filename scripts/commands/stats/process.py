#  -*- encoding: utf-8 -*-

from common.constants_and_variables import BotConstants


class ProcessStats(object):

    def __init__(self, update):
        self.update = update
        self.bot_constants = BotConstants()

    def process(self):
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.update.message.reply_text(message, reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)
