import datetime
import logging
from decimal import Decimal, ROUND_DOWN


class Common(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

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
