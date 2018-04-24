import unittest
from scripts.bot import FormatValue

class FormatValueTests(unittest.TestCase):

    format_value = FormatValue()

    def test_meters_to_kilometers(self):
        meters_to_kilometers = self.format_value.meters_to_kilometers(757.5)
        self.assertEqual(meters_to_kilometers, 0.7)

    def test_seconds_to_minutes(self):
        seconds_to_minutes = self.format_value.seconds_to_minutes(779)
        self.assertEqual(seconds_to_minutes, 12)

    def test_remove_decimal_point(self):
        remove_decimal_point = self.format_value.remove_decimal_point(55.9)
        self.assertEqual(remove_decimal_point, 55)

    def test_seconds_to_human_readable(self):
        seconds_to_human_readable = self.format_value.seconds_to_human_readable(658)
        self.assertEqual(seconds_to_human_readable, '0:10:58')

    def test_date_to_human_readable(self):
        date_to_human_readable = self.format_value.date_to_human_readable('2018-04-24T00:52:36Z')
        self.assertEqual(date_to_human_readable, '24/04/2018')

    def test_meters_per_second_to_kilometers(self):
        meters_per_second_to_kilometers = self.format_value.meters_per_second_to_kilometers(6.309)
        self.assertEqual(meters_per_second_to_kilometers, 22.7)