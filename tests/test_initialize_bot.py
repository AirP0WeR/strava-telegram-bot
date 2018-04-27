import unittest
import json
from scripts.bot import InitializeBot

class InitializeBotTests(unittest.TestCase):

    def setUp(self):
        self.initialize_bot = InitializeBot()

    def test_get_config(self):

        with open('config.json', 'r') as f:
            config = json.load(f)

        self.assertNotEquals(config['ENVIRONMENT'], " ")
        self.assertNotEquals(config['PROD_TELEGRAM_BOT_TOKEN'], " ")
        self.assertNotEquals(config['DEV_TELEGRAM_BOT_TOKEN'], " ")
        self.assertNotEquals(config['ATHLETES'], " ")
        self.assertNotEquals(config['ADMIN_USER_NAME'], " ")
        self.assertNotEquals(config['SHADOW_MODE'], " ")
        self.assertNotEquals(config['SHADOW_MODE_CHAT_ID'], " ")

    def test_strava_activity_hyperlink(self):
        activity_hyperlink = self.initialize_bot.strava_activity_hyperlink()
        self.assertEqual(activity_hyperlink, """[%s %s](https://www.strava.com/activities/%s)""")