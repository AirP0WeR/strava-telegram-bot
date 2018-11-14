#  -*- encoding: utf-8 -*-

from datetime import date
from os import sys, path

from stravalib.client import Client

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from stravalib import unithelper

from scripts.common.common import Common


class RunStatsFormat(object):

    def __init__(self):
        self.common = Common()

    def all_time_run_stats(self):
        return {
            'runs': 0,
            'distance': 0.0,
            'moving_time': 0,
            'elevation_gain': 0,
            'five': 0,
            'ten': 0,
            'hm': 0,
            'fm': 0,
            'ultra': 0
        }

    def ytd_run_stats(self):
        return {
            'runs': 0,
            'distance': 0.0,
            'moving_time': 0,
            'elevation_gain': 0,
            'five': 0,
            'ten': 0,
            'hm': 0,
            'fm': 0,
            'ultra': 0
        }

    def populate_run_stats(self, all_time_run_stats, ytd_run_stats):
        return "*All Time Stats:*\n\n" \
               "- _Runs_: {all_time_runs}\n" \
               "- _Distance_: {all_time_distance} km\n" \
               "- _Moving Time_: {all_time_moving_time} hours\n" \
               "- _Elevation Gain_: {all_time_elevation_gain} km\n" \
               "- _5's_: {all_time_five}\n" \
               "- _10's_: {all_time_ten}\n" \
               "- _HM's_: {all_time_hm}\n" \
               "- _FM's_: {all_time_fm}\n" \
               "- _Ultra's_: {all_time_ultra}\n\n" \
               "*Year to Date Stats:*\n\n" \
               "- _Runs_: {ytd_time_runs}\n" \
               "- _Distance_: {ytd_time_distance} km\n" \
               "- _Moving Time_: {ytd_time_moving_time} hours\n" \
               "- _Elevation Gain_: {ytd_time_elevation_gain} km\n" \
               "- _5's_: {ytd_time_five}\n" \
               "- _10's_: {ytd_time_ten}\n" \
               "- _HM's_: {ytd_time_hm}\n" \
               "- _FM's_: {ytd_time_fm}\n" \
               "- _Ultra's_: {ytd_time_ultra}\n\n".format(
            all_time_runs=all_time_run_stats['runs'],
            all_time_distance=self.common.meters_to_kilometers(all_time_run_stats['distance']),
            all_time_moving_time=self.common.seconds_to_human_readable(all_time_run_stats['moving_time']),
            all_time_elevation_gain=self.common.meters_to_kilometers(all_time_run_stats['elevation_gain']),
            all_time_five=all_time_run_stats['five'],
            all_time_ten=all_time_run_stats['ten'],
            all_time_hm=all_time_run_stats['hm'],
            all_time_fm=all_time_run_stats['fm'],
            all_time_ultra=all_time_run_stats['ultra'],
            ytd_time_runs=ytd_run_stats['runs'],
            ytd_time_distance=self.common.meters_to_kilometers(
                ytd_run_stats['distance']),
            ytd_time_moving_time=self.common.seconds_to_human_readable(
                ytd_run_stats['moving_time']),
            ytd_time_elevation_gain=self.common.meters_to_kilometers(
                ytd_run_stats['elevation_gain']),
            ytd_time_five=ytd_run_stats['five'],
            ytd_time_ten=ytd_run_stats['ten'],
            ytd_time_hm=ytd_run_stats['hm'],
            ytd_time_fm=ytd_run_stats['fm'],
            ytd_time_ultra=ytd_run_stats['ultra'])


class RunStats(object):
    def __init__(self, athlete_token):
        self.common = Common()
        self.strava_client = Client()
        self.strava_client.access_token = athlete_token

    def calculate_run_stats(self, current_year, activities, all_time_run_stats, ytd_run_stats):
        for activity in activities:
            if not self.common.is_flagged_or_private(activity):
                if self.common.is_activity_a_run(activity):
                    activity_year = activity.start_date_local.year

                    if activity_year == current_year:
                        ytd_run_stats['runs'] += 1
                    all_time_run_stats['runs'] += 1

                    if activity_year == current_year:
                        ytd_run_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                    all_time_run_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)

                    if activity_year == current_year:
                        ytd_run_stats['elevation_gain'] += int(activity.total_elevation_gain)
                    all_time_run_stats['elevation_gain'] += int(activity.total_elevation_gain)

                    if activity_year == current_year:
                        ytd_run_stats['distance'] += float(activity.distance)
                    all_time_run_stats['distance'] += float(activity.distance)

                    if 5000.0 <= float(activity.distance) < 10000.0:
                        if activity_year == current_year:
                            ytd_run_stats['five'] += 1
                        all_time_run_stats['five'] += 1
                    elif 10000.0 <= float(activity.distance) < 21000.0:
                        if activity_year == current_year:
                            ytd_run_stats['ten'] += 1
                        all_time_run_stats['ten'] += 1
                    elif 21000.0 < float(activity.distance) < 42000.0:
                        if activity_year == current_year:
                            ytd_run_stats['hm'] += 1
                        all_time_run_stats['hm'] += 1
                    elif 42000.0 < float(activity.distance) < 44000.0:
                        if activity_year == current_year:
                            ytd_run_stats['fm'] += 1
                        all_time_run_stats['fm'] += 1
                    elif float(activity.distance) > 44000.0:
                        if activity_year == current_year:
                            ytd_run_stats['ultra'] += 1
                        all_time_run_stats['ultra'] += 1

        return all_time_run_stats, ytd_run_stats

    def main(self):
        current_year = date.today().year
        activities = self.strava_client.get_activities()

        run_stats = []
        run_stats_format = RunStatsFormat()
        all_time_run_stats = run_stats_format.all_time_run_stats()
        ytd_run_stats = run_stats_format.ytd_run_stats()

        all_time_run_stats, ytd_run_stats = self.calculate_run_stats(current_year, activities, all_time_run_stats,
                                                                     ytd_run_stats)

        formulated_run_stats = run_stats_format.populate_run_stats(all_time_run_stats, ytd_run_stats)
        run_stats.append(formulated_run_stats)

        return run_stats
