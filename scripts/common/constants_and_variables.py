#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os


class BotConstants(object):
    QUERY_GET_ATHLETE_ID = "select athlete_id from strava_telegram_bot where telegram_username='{telegram_username}'"
    QUERY_GET_STRAVA_DATA = "select updated, strava_data from strava_telegram_bot where athlete_id={athlete_id}"
    QUERY_FETCH_TOKEN = "select access_token, refresh_token, expires_at from strava_telegram_bot where athlete_id={athlete_id}"
    QUERY_UPDATE_TOKEN = "UPDATE strava_telegram_bot SET access_token='{access_token}', refresh_token='{refresh_token}', expires_at={expires_at}, updated=now() where athlete_id={athlete_id}"
    QUERY_FETCH_UPDATE_INDOOR_RIDE = "select update_indoor_ride, update_indoor_ride_data from strava_telegram_bot where athlete_id={athlete_id}"
    QUERY_UPDATE_INDOOR_RIDE_DISABLE = "UPDATE strava_telegram_bot SET update_indoor_ride=False, update_indoor_ride_data=NULL where athlete_id={athlete_id}"
    QUERY_UPDATE_INDOOR_RIDE_ENABLE = "UPDATE strava_telegram_bot SET update_indoor_ride=True, update_indoor_ride_data='{update_indoor_ride_data}' where athlete_id={athlete_id}"
    QUERY_GET_ATHLETES = "select name from strava_telegram_bot"

    MESSAGE_START_COMMAND = "Hi {first_name}! Type '/' to get the list of command(s)."
    MESSAGE_STATS_COMMAND = "Hi {first_name}! Give me a moment while I fetch your stats."
    MESSAGE_STATS_MAIN_KEYBOARD_MENU = "Choose an activity type to view your stats:"
    MESSAGE_STATS_RIDE_KEYBOARD_MENU = "Choose the type of stat you want to see:"
    MESSAGE_STATS_NOT_UPDATED = "Stats are not synced yet. Please check again after a minute."
    MESSAGE_UPDATE_STATS_FAILED = "Failed to update stats."
    MESSAGE_UPDATE_STATS_STARTED = "Refreshing.. Check stats after a minute or two."
    MESSAGE_UPDATE_STATS_STARTED_ALL = "Refreshing.."
    MESSAGE_UNREGISTERED_ATHLETE = "Hi {first_name}! You are not a registered user yet.\n\nVisit the following link to register: {registration_url}\n\nPing {admin_user_name} in case you face any issue."
    MESSAGE_EXIT_BUTTON = "Thank you!"
    MESSAGE_SHOULD_UPDATE_INDOOR_RIDE_DISABLE = "You have automated update of Indoor Rides with the below configuration:\n\n{configuration}\n\nDo you want to disable it?"
    MESSAGE_UPDATE_INDOOR_RIDE_DISABLE_CANCEL = "Auto update of Indoor Rides is still enabled. Thank you!"
    MESSAGE_UPDATE_INDOOR_RIDE_CHOOSE_ACTIVITY_NAME = "Choose the activity name: (Send /cancel to cancel ongoing operation)"
    MESSAGE_CANCEL_CURRENT_OPERATION = "Cancelled current operation."
    MESSAGE_UPDATE_INDOOR_RIDE_DISABLED = "Disabled auto update of Indoor Rides."
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CHOOSE_BIKE = "Choose the bike you want to set for Indoor Rides: (Send /cancel to cancel ongoing operation)"
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CONFIRMATION = "Are you sure you want to enable auto updates of Indoor Rides with the below configuration?\n\n{configuration}"
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_INSUFFICIENT_INFORMATION = 'Insufficient information to enable auto updates of Indoor Rides. Bye!'
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_ENABLED = "Enabled auto update of Indoor Rides."
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CANCELLED = "Cancelled setup for auto update of Indoor Rides"

    API_TOKEN_EXCHANGE = 'https://www.strava.com/oauth/token'
    API_WEBHOOK_UPDATE_STATS = "https://strava-telegram-webhooks-stage.herokuapp.com/stats/{athlete_id}"
    API_WEBHOOK_UPDATE_STATS_ALL = "https://strava-telegram-webhooks-stage.herokuapp.com/stats/all"

    KEYBOARD_STATS_MAIN_KEYBOARD_MENU = InlineKeyboardMarkup([[InlineKeyboardButton("Ride", callback_data='stats_ride'),
                                                               InlineKeyboardButton("Run", callback_data='stats_run')],
                                                              [InlineKeyboardButton("Exit",
                                                                                    callback_data='stats_exit')]])

    KEYBOARD_STATS_RIDE_KEYBOARD_MENU = InlineKeyboardMarkup(
        [[InlineKeyboardButton("All Time", callback_data='stats_ride_all_time'),
          InlineKeyboardButton("Year to Date", callback_data='stats_ride_ytd'),
          InlineKeyboardButton("Previous Year", callback_data='stats_ride_py')],
         [InlineKeyboardButton("Current Month", callback_data='stats_ride_cm'),
          InlineKeyboardButton("Previous Month", callback_data='stats_ride_pm')],
         [InlineKeyboardButton("Back", callback_data='stats_back'),
          InlineKeyboardButton("Exit", callback_data='stats_exit')]])

    KEYBOARD_STATS_RUN_KEYBOARD_MENU = InlineKeyboardMarkup(
        [[InlineKeyboardButton("All Time", callback_data='stats_run_all_time'),
          InlineKeyboardButton("Year to Date", callback_data='stats_run_ytd'),
          InlineKeyboardButton("Previous Year", callback_data='stats_run_py')],
         [InlineKeyboardButton("Current Month", callback_data='stats_run_cm'),
          InlineKeyboardButton("Previous Month", callback_data='stats_run_pm')],
         [InlineKeyboardButton("Back", callback_data='stats_back'),
          InlineKeyboardButton("Exit", callback_data='stats_exit')]])

    KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_DISABLE_PROMPT = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Yes", callback_data='auto_update_indoor_ride_disable'),
          InlineKeyboardButton("No", callback_data='auto_update_indoor_ride_ignore')]])

    KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_NAME = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Indoor Ride", callback_data='auto_update_indoor_ride_name_indoor_ride'),
          InlineKeyboardButton("Indoor Cycling", callback_data='auto_update_indoor_ride_name_indoor_cycling')],
         [InlineKeyboardButton("Morning/Afternoon/Evening/Night Ride",
                               callback_data='auto_update_indoor_ride_name_automatic')],
         [InlineKeyboardButton("Skip this field", callback_data='auto_update_indoor_ride_name_skip')]])

    KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_CONFIRMATION = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Yes", callback_data='auto_update_indoor_ride_update_confirm_yes'),
          InlineKeyboardButton("No", callback_data='auto_update_indoor_ride_confirm_no')]])


class BotVariables(object):
    database_url = os.environ.get('DATABASE_URL')
    admin_user_name = os.environ.get('ADMIN_USER_NAME')
    app_name = os.environ.get('APP_NAME')
    port = int(os.environ.get('PORT'))
    registration_url = os.environ.get('REGISTRATION_URL')
    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    admins = os.environ.get('ADMINS', '').split(',')
