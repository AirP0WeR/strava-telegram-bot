import logging
from datetime import date

import dateutil.parser

from common import Common
from strava_api import StravaApi


class Stats(StravaApi, Common):

    def __init__(self, athlete_token, command):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.command = command
        StravaApi.__init__(self, athlete_token)

    def calculate_stats(self, current_year, athlete_activities, all_time_stats, ytd_stats):
        for activity in athlete_activities:
            if not self.is_flagged_or_private(activity):
                if activity['type'] == 'Ride' or activity['type'] == 'VirtualRide':

                    activity_year = int((dateutil.parser.parse(activity['start_date_local'])).strftime('%Y'))

                    if activity_year == current_year:
                        ytd_stats['rides'] += 1
                    all_time_stats['rides'] += 1

                    if activity_year == current_year:
                        ytd_stats['moving_time'] += activity['moving_time']
                    all_time_stats['moving_time'] += activity['moving_time']

                    if activity_year == current_year:
                        ytd_stats['elevation_gain'] += activity['total_elevation_gain']
                    all_time_stats['elevation_gain'] += activity['total_elevation_gain']

                    distance = float(activity['distance'])

                    if activity_year == current_year:
                        ytd_stats['distance'] += distance
                    all_time_stats['distance'] += distance

                    if 50000.0 <= distance < 100000.0:
                        if activity_year == current_year:
                            ytd_stats['fifties'] += 1
                        all_time_stats['fifties'] += 1
                    elif 100000.0 <= distance < 150000.0:
                        if activity_year == current_year:
                            ytd_stats['hundreds'] += 1
                        all_time_stats['hundreds'] += 1
                    elif 150000.0 < distance < 200000.0:
                        if activity_year == current_year:
                            ytd_stats['one_hundred_fifties'] += 1
                            ytd_stats['hundreds'] += 1
                        all_time_stats['one_hundred_fifties'] += 1
                        all_time_stats['hundreds'] += 1
                    elif distance > 200000.0:
                        if activity_year == current_year:
                            ytd_stats['two_hundreds'] += 1
                            ytd_stats['hundreds'] += 1
                        all_time_stats['two_hundreds'] += 1
                        all_time_stats['hundreds'] += 1

                    if activity['trainer'] or activity['type'] == 'VirtualRide':
                        if activity_year == current_year:
                            ytd_stats['indoor_distance'] += self.meters_to_kilometers(activity['distance'])
                            ytd_stats['indoor_time'] += activity['moving_time']
                            ytd_stats['indoor_rides'] += 1
                        all_time_stats['indoor_distance'] += self.meters_to_kilometers(activity['distance'])
                        all_time_stats['indoor_time'] += activity['moving_time']
                        all_time_stats['indoor_rides'] += 1

        return all_time_stats, ytd_stats

    def get_stats(self, current_year):

        all_time_stats = {
            'rides': 0,
            'indoor_rides': 0,
            'distance': 0,
            'indoor_distance': 0,
            'moving_time': 0,
            'indoor_time': 0,
            'elevation_gain': 0,
            'fifties': 0,
            'hundreds': 0,
            'one_hundred_fifties': 0,
            'two_hundreds': 0
        }

        ytd_stats = {
            'rides': 0,
            'indoor_rides': 0,
            'distance': 0,
            'indoor_distance': 0,
            'moving_time': 0,
            'indoor_time': 0,
            'elevation_gain': 0,
            'fifties': 0,
            'hundreds': 0,
            'one_hundred_fifties': 0,
            'two_hundreds': 0
        }

        page = 1
        while page:
            athlete_activities = self.get_athlete_activities("200", page)
            if len(athlete_activities) == 0:
                break
            all_time_stats, ytd_stats = self.calculate_stats(current_year, athlete_activities, all_time_stats,
                                                             ytd_stats)
            page += 1

        return all_time_stats, ytd_stats

    def main(self):

        all_time_stats, ytd_stats = self.get_stats(date.today().year)
        message = "*All Time Stats:*\n\n" \
                  "- _Rides_: %s (Includes %s Indoors)\n" \
                  "- _Distance_: %s kms (Includes %s kms of Indoors)\n" \
                  "- _Moving Time_: %s hours (Includes %s hours of Indoors)\n" \
                  "- _Elevation Gain_: %s kms\n" \
                  "- _50's_: %s\n" \
                  "- _100's_: %s (Includes %s _150's_ & %s _200's_)\n\n" \
                  "*Year to Date Stats:*\n\n" \
                  "- _Rides_: %s (Includes %s Indoors)\n" \
                  "- _Distance_: %s kms (Includes %s kms of Indoors)\n" \
                  "- _Moving Time_: %s hours (Includes %s hours of Indoors)\n" \
                  "- _Elevation Gain_: %s kms\n" \
                  "- _50's_: %s\n" \
                  "- _100's_: %s (Includes %s _150's_ & %s _200's_)" % \
                  (all_time_stats['rides'],
                   all_time_stats['indoor_rides'],
                   self.meters_to_kilometers(all_time_stats['distance']),
                   all_time_stats['indoor_distance'],
                   self.seconds_to_human_readable(all_time_stats['moving_time']),
                   self.seconds_to_human_readable(all_time_stats['indoor_time']),
                   self.meters_to_kilometers(all_time_stats['elevation_gain']),
                   all_time_stats['fifties'],
                   all_time_stats['hundreds'],
                   all_time_stats['one_hundred_fifties'],
                   all_time_stats['two_hundreds'],
                   ytd_stats['rides'],
                   ytd_stats['indoor_rides'],
                   self.meters_to_kilometers(ytd_stats['distance']),
                   ytd_stats['indoor_distance'],
                   self.seconds_to_human_readable(ytd_stats['moving_time']),
                   self.seconds_to_human_readable(ytd_stats['indoor_time']),
                   self.meters_to_kilometers(ytd_stats['elevation_gain']),
                   ytd_stats['fifties'],
                   ytd_stats['hundreds'],
                   ytd_stats['one_hundred_fifties'],
                   ytd_stats['two_hundreds'])

        return message
