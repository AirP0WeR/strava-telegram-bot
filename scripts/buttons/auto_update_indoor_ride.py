#  -*- encoding: utf-8 -*-

import json
from collections import defaultdict
from os import sys, path

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.constants_and_variables import BotConstants, BotVariables
from scripts.common.operations import Operations
from scripts.clients.strava import StravaClient
from scripts.clients.database import DatabaseClient


class AutoUpdateIndoorRide(object):

    def __init__(self, bot, update, user_data, chosen_option):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_constants = BotConstants()
        self.bot_variables = BotVariables()
        self.operations = Operations()
        self.query = self.update.callback_query
        self.chosen_option = chosen_option
        self.chat_id = self.query.message.chat_id
        self.message_id = self.query.message.message_id
        self.database_client = DatabaseClient()

    def auto_update_indoor_ride_disable(self):
        self.database_client.write_operation(self.bot_constants.QUERY_UPDATE_INDOOR_RIDE_DISABLE.format(
            athlete_id=self.user_data['auto_update_indoor_ride']['athlete_id']))
        self.user_data.clear()
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_UPDATE_INDOOR_RIDE_DISABLED, chat_id=self.chat_id,
                                   message_id=self.message_id)

    def auto_update_indoor_ride_ignore(self):
        self.user_data.clear()
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_UPDATE_INDOOR_RIDE_DISABLE_CANCEL,
                                   chat_id=self.chat_id, message_id=self.message_id)

    def auto_update_indoor_ride_name_indoor_ride(self):
        self.user_data['auto_update_indoor_ride'].update({'name': 'Indoor Ride'})
        self.get_bikes()

    def auto_update_indoor_ride_name_indoor_cycling(self):
        self.user_data['auto_update_indoor_ride'].update({'name': 'Indoor Cycling'})
        self.get_bikes()

    def auto_update_indoor_ride_name_automatic(self):
        self.user_data['auto_update_indoor_ride'].update({'name': 'Automatic'})
        self.get_bikes()

    def auto_update_indoor_ride_name_skip(self):
        self.user_data['auto_update_indoor_ride'].update({'name': None})
        self.get_bikes()

    def get_bikes(self):
        strava_client = StravaClient().get_client_with_token(self.user_data['auto_update_indoor_ride']['athlete_token'])
        athlete = strava_client.get_athlete()
        bikes = dict()
        count = 1
        for bike in athlete.bikes:
            bikes.update({count: {'bike_name': bike.name, 'bike_id': bike.id}})
            count += 1
        if len(bikes) > 0:
            bikes_list = []
            for sl_no in bikes:
                bikes_list += [InlineKeyboardButton(text=sl_no, callback_data=bikes[sl_no]['bike_id'])]
            keyboard_bikes = InlineKeyboardMarkup(inline_keyboard=[bikes_list])
            list_bikes = ""
            for sl_no in bikes:
                list_bikes += "{sl_no}. {bike_name}\n".format(sl_no=sl_no, bike_name=bikes[sl_no]['bike_name'])
            self.user_data['auto_update_indoor_ride'].update({'gear_id': bikes})
            self.bot.send_message(text=list_bikes, chat_id=self.chat_id)
            self.bot.edit_message_text(text=self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CHOOSE_BIKE,
                                       chat_id=self.chat_id, message_id=self.message_id, reply_markup=keyboard_bikes)
        else:
            self.user_data['auto_update_indoor_ride'].update({'bike': None})
            self.update_indoor_ride_setup_confirmation()

    def update_indoor_ride_setup_confirmation(self):
        found = True
        if 'name' not in self.user_data['auto_update_indoor_ride']:
            if 'gear_id' not in self.user_data['auto_update_indoor_ride']:
                found = False
        self.bot.deleteMessage(self.chat_id, self.message_id)
        if found:
            self.bot.send_message(text=self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CONFIRMATION,
                                  chat_id=self.chat_id,
                                  reply_markup=self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_CONFIRMATION)
        else:
            self.user_data.clear()
            self.bot.send_message(text=self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_INSUFFICIENT_INFORMATION,
                                  chat_id=self.chat_id)

    def auto_update_indoor_ride_update_confirm_yes(self):
        update_indoor_ride_data = dict()
        if 'name' in self.user_data['auto_update_indoor_ride']:
            update_indoor_ride_data.update({'name': self.user_data['auto_update_indoor_ride']['name']})
        if 'gear_id' in self.user_data['auto_update_indoor_ride']:
            update_indoor_ride_data.update({'gear_id': self.user_data['auto_update_indoor_ride']['gear_id']})

        self.database_client.write_operation(self.bot_constants.QUERY_UPDATE_INDOOR_RIDE_ENABLE.format(
            update_indoor_ride_data=json.dumps(update_indoor_ride_data),
            athlete_id=self.user_data['auto_update_indoor_ride']['athlete_id']))

        self.user_data.clear()
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_ENABLED,
                                   chat_id=self.chat_id, message_id=self.message_id)

    def auto_update_indoor_ride_confirm_no(self):
        self.user_data.clear()
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CANCELLED,
                                   chat_id=self.chat_id, message_id=self.message_id)

    def exit_button(self):
        self.user_data.clear()
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_EXIT_BUTTON, chat_id=self.chat_id,
                                   message_id=self.message_id)

    def process(self):
        options = defaultdict(lambda: self.exit_button, {
            'auto_update_indoor_ride_disable': self.auto_update_indoor_ride_disable,
            'auto_update_indoor_ride_ignore': self.auto_update_indoor_ride_ignore,
            'auto_update_indoor_ride_name_indoor_ride': self.auto_update_indoor_ride_name_indoor_ride,
            'auto_update_indoor_ride_name_indoor_cycling': self.auto_update_indoor_ride_name_indoor_cycling,
            'auto_update_indoor_ride_name_automatic': self.auto_update_indoor_ride_name_automatic,
            'auto_update_indoor_ride_name_skip': self.auto_update_indoor_ride_name_skip,
            'update_indoor_ride_setup_confirmation': self.update_indoor_ride_setup_confirmation,
            'auto_update_indoor_ride_update_confirm_yes': self.auto_update_indoor_ride_update_confirm_yes,
            'auto_update_indoor_ride_confirm_no': self.auto_update_indoor_ride_confirm_no
        })

        options[self.chosen_option]()
