import unittest
from bot import InitializeBot

class StravaTelegramBotTests(unittest.TestCase):

    def test_strava_activity_hyperlink(self):
        activity_hyperlink = InitializeBot().strava_activity_hyperlink()
        self.assertEqual(activity_hyperlink, """[%s %s](https://www.strava.com/activities/%s)""")