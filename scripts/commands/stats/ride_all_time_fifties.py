#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class RideAllTimeFiftiesStats(object):
    MESSAGE_RIDE_ALL_TIME_FIFTIES_STATS = "{serial_no}. [{activity_name}](https://www.strava.com/activities/{activity_id}) ({activity_date})\n"

    def __init__(self):
        self.operations = Operations()

    @staticmethod
    def input():
        serial_no = 0
        message = "*50 km Rides:*\n\n"
        ride_fifties_list = list()
        return serial_no, message, ride_fifties_list

    def calculate(self, serial_no, message, ride_fifties_list, activity):
        if 50000 <= float(activity.distance) < 100000:
            serial_no += 1
            message += self.MESSAGE_RIDE_ALL_TIME_FIFTIES_STATS.format(
                serial_no=serial_no,
                activity_name=activity.name,
                activity_id=activity.id,
                activity_date=activity.start_date_local.date())

            if serial_no % 25 == 0:
                ride_fifties_list.append(message)
                message = ""

        return serial_no, message, ride_fifties_list
