#  -*- encoding: utf-8 -*-

import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class BotConstants(object):
    QUERY_GET_ATHLETE_ID = "select athlete_id from strava_telegram_bot where telegram_username='{telegram_username}' and active=TRUE"
    QUERY_GET_STRAVA_DATA = "select strava_data from strava_telegram_bot where telegram_username='{telegram_username}'"
    QUERY_FETCH_TOKEN = "select access_token, refresh_token, expires_at from strava_telegram_bot where athlete_id={athlete_id}"
    QUERY_UPDATE_TOKEN = "UPDATE strava_telegram_bot SET access_token='{access_token}', refresh_token='{refresh_token}', expires_at={expires_at}, updated=now() where athlete_id={athlete_id}"
    QUERY_FETCH_UPDATE_INDOOR_RIDE = "select update_indoor_ride, update_indoor_ride_data from strava_telegram_bot where athlete_id={athlete_id}"
    QUERY_UPDATE_INDOOR_RIDE_DISABLE = "UPDATE strava_telegram_bot SET update_indoor_ride=False, update_indoor_ride_data=NULL where athlete_id={athlete_id}"
    QUERY_UPDATE_INDOOR_RIDE_ENABLE = "UPDATE strava_telegram_bot SET update_indoor_ride=True, update_indoor_ride_data='{update_indoor_ride_data}', chat_id='{chat_id}' where athlete_id={athlete_id}"
    QUERY_GET_ATHLETES = "select name from strava_telegram_bot order by created"
    QUERY_ACTIVITY_SUMMARY_ENABLE = "UPDATE strava_telegram_bot SET enable_activity_summary=True, chat_id='{chat_id}' where athlete_id={athlete_id}"
    QUERY_ACTIVITY_SUMMARY_DISABLE = "UPDATE strava_telegram_bot SET enable_activity_summary=False, chat_id=NULL where athlete_id={athlete_id}"
    QUERY_ACTIVITY_SUMMARY = "select enable_activity_summary from strava_telegram_bot where athlete_id={athlete_id}"
    QUERY_ACTIVITY_SUMMARY_BY_TELEGRAM_USERNAME = "select enable_activity_summary from strava_telegram_bot where telegram_username='{telegram_username}'"  # Promotion - Temporary code

    MESSAGE_START_COMMAND = "Hi {first_name}! Type '/' to get the list of command(s) I understand or click /help to know more."
    MESSAGE_STATS_MAIN_KEYBOARD_MENU = "Choose an activity type to view your stats:"
    MESSAGE_STATS_SUB_KEYBOARD_MENU = "Choose the type of stat you want to see:"
    MESSAGE_STATS_NOT_UPDATED = "Stats are not synced yet. Please check again after a minute."
    MESSAGE_UPDATE_STATS_FAILED = "Hi {first_name}! Failed to update stats."
    MESSAGE_UPDATE_STATS_STARTED = "Hi {first_name}! Refreshing.. Check stats after a minute or two."
    MESSAGE_UPDATE_STATS_STARTED_ALL = "Hi {first_name}! Refreshing.."
    MESSAGE_UNREGISTERED_ATHLETE = "Hi {first_name}! You are not a registered user yet.\n\nVisit the following link to register: {registration_url}\n\nContact {admin_user_name} in case you face any issues.\n\nAlternatively, you can select a topic below for help."
    MESSAGE_EXIT_BUTTON = "Thank you!"
    MESSAGE_SHOULD_UPDATE_INDOOR_RIDE_DISABLE = "Hi {first_name}! You have automated update of Indoor Rides with the below configuration:\n{configuration}\n\nDo you want to disable it?"
    MESSAGE_UPDATE_INDOOR_RIDE_DISABLE_CANCEL = "Auto update of Indoor Rides is still enabled. Thank you!"
    MESSAGE_UPDATE_INDOOR_RIDE_CHOOSE_ACTIVITY_NAME = "Hi {first_name}! Choose the activity name: (Send /cancel to cancel ongoing operation)"
    MESSAGE_CANCEL_CURRENT_OPERATION = "Cancelled current operation."
    MESSAGE_UPDATE_INDOOR_RIDE_DISABLED = "Disabled auto update of Indoor Rides."

    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CHOOSE_BIKE = "Choose the bike you want to set for Indoor Rides: (Send /cancel to cancel ongoing operation)"
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CONFIRMATION = "Are you sure you want to enable auto updates of Indoor Rides with the below configuration?\n\n{configuration}"
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_INSUFFICIENT_INFORMATION = 'Insufficient information to enable auto updates of Indoor Rides. Bye!'
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_ENABLED = "Enabled auto update of Indoor Rides."
    MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CANCELLED = "Cancelled setup for auto update of Indoor Rides"

    MESSAGE_FETCHING_REGISTERED_ATHLETES = "Hi {first_name}! Fetching the list of registered athletes."

    MESSAGE_ACTIVITY_SUMMARY_CONFIRMATION = "Hi {first_name}! Do you want to receive Activity Summary for your activities?"
    MESSAGE_ACTIVITY_SUMMARY_ENABLED = "Enabled Activity Summary.\n\nNote: Do not delete this chat to continue to receive updates. As per Telegram policy, Bots cannot send messages if the chat is deleted."
    MESSAGE_ACTIVITY_SUMMARY_IGNORE = "Activity Summary setup cancelled."
    MESSAGE_ACTIVITY_SUMMARY_DISABLED = "Disabled Activity Summary."
    MESSAGE_ACTIVITY_SUMMARY_DISABLE_IGNORE = "Activity Summary is still enabled. Thank you!"
    MESSAGE_ACTIVITY_SUMMARY_SHOULD_DISABLE = "Hi {first_name}! You have enabled Activity Summary. Do you want to disable it?"

    MESSAGE_HELP_TOPICS = "Hi {first_name}! Select a topic below for help."
    MESSAGE_HELP_EXIT = "Goodbye!"
    MESSAGE_HELP_REGISTRATION_DEVICE = "Choose the type of device you use:"
    MESSAGE_HELP_COMMANDS = "/stats - Get your Monthly, Yearly and All Time Statistics and compare your monthly/yearly statistics with your previous month/year.\n\n" \
                            "/activity_summary - Get your activity summary as soon as you finish your activity\n\n" \
                            "/auto_update_indoor_ride - Get your activity Name / Bike updated automatically for your indoor rides\n\n" \
                            "/refresh_stats - Force refresh stats. Use this only if you find any discrepancy in your stats."

    API_TOKEN_EXCHANGE = 'https://www.strava.com/oauth/token'
    API_TELEGRAM_SEND_MESSAGE = "https://api.telegram.org/bot{bot_token}/sendMessage"

    KEYBOARD_STATS_MAIN_KEYBOARD_MENU = InlineKeyboardMarkup([[InlineKeyboardButton("Ride", callback_data='stats_ride'),
                                                               InlineKeyboardButton("Run", callback_data='stats_run'),
                                                               InlineKeyboardButton("Swim",
                                                                                    callback_data='stats_swim')],
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

    KEYBOARD_STATS_SWIM_KEYBOARD_MENU = InlineKeyboardMarkup(
        [[InlineKeyboardButton("All Time", callback_data='stats_swim_all_time'),
          InlineKeyboardButton("Year to Date", callback_data='stats_swim_ytd'),
          InlineKeyboardButton("Previous Year", callback_data='stats_swim_py')],
         [InlineKeyboardButton("Current Month", callback_data='stats_swim_cm'),
          InlineKeyboardButton("Previous Month", callback_data='stats_swim_pm')],
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

    KEYBOARD_ENABLE_ACTIVITY_SUMMARY_CONFIRMATION = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Yes", callback_data='activity_summary_enable'),
          InlineKeyboardButton("No", callback_data='activity_summary_ignore')]])

    KEYBOARD_ACTIVITY_SUMMARY_DISABLE_CONFIRMATION = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Yes", callback_data='activity_summary_disable'),
          InlineKeyboardButton("No", callback_data='activity_summary_disable_ignore')]])

    KEYBOARD_HELP_MENU = InlineKeyboardMarkup([[InlineKeyboardButton("Registration", callback_data='help_registration'),
                                                InlineKeyboardButton("Bot Commands", callback_data='help_commands')],
                                               [InlineKeyboardButton("Exit", callback_data='help_exit')]])

    KEYBOARD_HELP_REGISTRATION = InlineKeyboardMarkup(
        [[InlineKeyboardButton("iOS", callback_data='help_registration_ios'),
          InlineKeyboardButton("Android", callback_data='help_registration_android')],
         [InlineKeyboardButton("Exit", callback_data='help_exit')]])


class BotVariables(object):
    crypt_key_length = int(os.environ.get('CRYPT_KEY_LENGTH'))
    crypt_key = os.environ.get('CRYPT_KEY')
    database_url = os.environ.get('DATABASE_URL')
    admin_user_name = os.environ.get('ADMIN_USER_NAME')
    app_name = os.environ.get('APP_NAME')
    port = int(os.environ.get('PORT'))
    registration_url = os.environ.get('REGISTRATION_URL')
    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    admins = os.environ.get('ADMINS', '').split(',')
    shadow_mode = os.environ.get('SHADOW_MODE')
    shadow_mode_chat_id = os.environ.get('SHADOW_MODE_CHAT_ID')
    iron_cache_project_id = os.environ.get('IRON_CACHE_PROJECT_ID')
    iron_cache_token = os.environ.get('IRON_CACHE_TOKEN')
    api_update_stats_webhook = os.environ.get('UPDATE_STATS_WEBHOOK_API')
    api_update_stats_all_webhook = os.environ.get('UPDATE_STATS_ALL_WEBHOOK_API')
