#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class RideHundredsStats(object):
    MESSAGE_RIDE_HUNDREDS_STATS = "{serial_no}. [{activity_name}](https://www.strava.com/activities/{activity_id}) ({activity_date})\n"

    def __init__(self):
        self.operations = Operations()

    @staticmethod
    def input():
        serial_no = 0
        list_ride_hundreds_stats = list()
        return serial_no, list_ride_hundreds_stats

    def calculate(self, serial_no, input_list_ride_hundreds_stats, activity):
        if float(activity.distance) >= 100000:
            serial_no += 1
            input_list_ride_hundreds_stats.append(self.MESSAGE_RIDE_HUNDREDS_STATS.format(
                serial_no=serial_no,
                activity_name=activity.name,
                activity_id=activity.id,
                activity_date=activity.start_date_local.date()
            ))

        return serial_no, input_list_ride_hundreds_stats
