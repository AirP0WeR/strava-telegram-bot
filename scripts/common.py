import datetime
import logging
import time
from decimal import Decimal, ROUND_DOWN


class Common(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def meters_to_kilometers(distance):
        return float((Decimal(distance / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN))

    @staticmethod
    def seconds_to_minutes(time_in_seconds):
        return time_in_seconds / 60

    @staticmethod
    def remove_decimal_point(number):
        return int(number)

    @staticmethod
    def seconds_to_human_readable(time_in_seconds):
        return str(datetime.timedelta(seconds=time_in_seconds))

    @staticmethod
    def date_to_human_readable(activity_date):
        return time.strftime("%d/%m/%Y", time.strptime(activity_date[:19], "%Y-%m-%dT%H:%M:%S"))

    @staticmethod
    def date_to_human_readable_with_time(activity_date):
        return time.strftime("%d/%m/%Y %H:%M:%S", time.strptime(activity_date[:19], "%Y-%m-%dT%H:%M:%S"))

    @staticmethod
    def meters_per_second_to_kilometers(speed):
        return float((Decimal(speed * 3.6)).quantize(Decimal('.1'), rounding=ROUND_DOWN))

    @staticmethod
    def strava_activity_hyperlink():
        return """[%s %s](https://www.strava.com/activities/%s)"""

    @staticmethod
    def is_flagged_or_private(activity):
        if ('flagged' in activity) and (activity['flagged']):
            return True

        if ('private' in activity) and (activity['private']):
            return True

        return False
