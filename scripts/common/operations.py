#  -*- encoding: utf-8 -*-

import datetime
from decimal import Decimal, ROUND_DOWN


class Operations(object):

    @staticmethod
    def meters_to_kilometers(distance):
        return float((Decimal(distance / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN))

    @staticmethod
    def remove_decimal_point(number):
        return int(number)

    @staticmethod
    def seconds_to_human_readable(time_in_seconds):
        return str(datetime.timedelta(seconds=time_in_seconds))

    @staticmethod
    def strava_activity_hyperlink():
        return """[%s %s](https://www.strava.com/activities/%s)"""

    @staticmethod
    def is_flagged_or_private(activity):
        return True if (activity.flagged or activity.private) else False

    @staticmethod
    def is_activity_a_ride(activity):
        return True if (activity.type == 'Ride' or activity.type == 'VirtualRide') else False

    @staticmethod
    def is_activity_a_run(activity):
        return True if (activity.type == 'Run' or activity.type == 'VirtualRun') else False

    @staticmethod
    def is_indoor(activity):
        return True if (activity.trainer or activity.type == 'VirtualRide') else False
