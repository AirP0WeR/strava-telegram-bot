#  -*- encoding: utf-8 -*-

from buttons.auto_update_indoor_ride import AutoUpdateIndoorRide
from buttons.stats import Stats
from scripts.common.constants_and_variables import BotConstants


class HandleButtons(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_constants = BotConstants()
        self.query = self.update.callback_query
        self.chosen_option = self.query.data
        self.chat_id = self.query.message.chat_id
        self.message_id = self.query.message.message_id

    def process(self):
        if self.chosen_option.startswith('stats'):
            stats = Stats(self.bot, self.update, self.user_data)
            stats.process()
        elif self.chosen_option.startswith('auto_update_indoor_ride'):
            setup = AutoUpdateIndoorRide(self.bot, self.update, self.user_data, self.chosen_option)
            setup.process()
        elif 'auto_update_indoor_ride' in self.user_data:
            if 'gear_id' in self.user_data['auto_update_indoor_ride']:
                self.user_data['auto_update_indoor_ride']['gear_id'] = self.chosen_option
                self.chosen_option = 'auto_update_indoor_ride_setup_confirmation'
                setup = AutoUpdateIndoorRide(self.bot, self.update, self.user_data, self.chosen_option)
                setup.process()
