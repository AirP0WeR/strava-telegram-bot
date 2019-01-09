#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from telegram import InlineKeyboardButton
import os


class BotConstants(object):
    QUERY_FETCH_TOKEN = "select athlete_id, access_token, refresh_token, expires_at from strava_telegram_bot where telegram_username='{telegram_username}'"
    QUERY_UPDATE_TOKEN = "UPDATE strava_telegram_bot SET access_token='{access_token}', refresh_token='{refresh_token}', expires_at={expires_at}, updated=now() where athlete_id={athlete_id}"

    MESSAGE_START_COMMAND = "Hi {first_name}! Type '/' to get the list of command(s)."
    MESSAGE_STATS_COMMAND = "Hi {first_name}! Give me a minute or two while I fetch your data."
    MESSAGE_STATS_MAIN_KEYBOARD_MENU = "Choose an activity type to view your stats:"
    MESSAGE_STATS_RIDE_KEYBOARD_MENU = "Choose the type of stat you want to see:"
    MESSAGE_UNREGISTERED_ATHLETE = "Hi {first_name}! You are not a registered user yet.\n\nVisit the following link to register: {registration_url}\n\nPing {admin_user_name} in case you face any issue."
    MESSAGE_EXIT_BUTTON = "Thank you!"

    API_TOKEN_EXCHANGE = 'https://www.strava.com/oauth/token'

    STATS_MAIN_KEYBOARD_MENU = [[InlineKeyboardButton("Ride", callback_data='stats_ride'),
                                 InlineKeyboardButton("Run", callback_data='stats_run')],
                                [InlineKeyboardButton("Exit", callback_data='exit')]]

    STATS_RIDE_KEYBOARD_MENU = [[InlineKeyboardButton("All Time", callback_data='stats_ride_all_time'),
                                 InlineKeyboardButton("Year to Date", callback_data='stats_ride_ytd'),
                                 InlineKeyboardButton("Previous Year", callback_data='stats_ride_py')],
                                [InlineKeyboardButton("Current Month", callback_data='stats_ride_cm'),
                                 InlineKeyboardButton("Previous Month", callback_data='stats_ride_pm')],
                                [InlineKeyboardButton("Back", callback_data='back'),
                                 InlineKeyboardButton("Exit", callback_data='exit')]]

    STATS_RUN_KEYBOARD_MENU = [[InlineKeyboardButton("All Time", callback_data='stats_run_all_time'),
                                InlineKeyboardButton("Year to Date", callback_data='stats_run_ytd'),
                                InlineKeyboardButton("Previous Year", callback_data='stats_run_py')],
                               [InlineKeyboardButton("Current Month", callback_data='stats_run_cm'),
                                InlineKeyboardButton("Previous Month", callback_data='stats_run_pm')],
                               [InlineKeyboardButton("Back", callback_data='back'),
                                InlineKeyboardButton("Exit", callback_data='exit')]]


class BotVariables(object):
    database_url = os.environ['DATABASE_URL']
    admin_user_name = os.environ['ADMIN_USER_NAME']
    app_name = os.environ.get('APP_NAME')
    port = int(os.environ.get('PORT'))
    registration_url = os.environ['REGISTRATION_URL']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
