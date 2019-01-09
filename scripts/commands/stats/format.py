#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class FormatStats(object):

    def __init__(self, calculated_stats):
        self.calculated_stats = calculated_stats
        self.operations = Operations()

    @staticmethod
    def output_ride():
        return "*Ride - {stats_type}:*\n\n" \
               "- _Rides_: {total} (Includes {total_indoor} Indoors)\n" \
               "- _Distance_: {distance} km (Includes {indoor_distance} km of Indoors)\n" \
               "- _Moving Time_: {moving_time} hours (Includes {indoor_moving_time} hours of Indoors)\n" \
               "- _Elevation Gain_: {elevation_gain} km\n" \
               "- _Biggest Ride_: {biggest_ride} km\n" \
               "- _50's_: {fifties}\n" \
               "- _100's_: {hundreds}"

    @staticmethod
    def output_run():
        return "*Run - {stats_type}:*\n\n" \
               "- _Runs_: {total} (Includes {total_indoor} Indoors)\n" \
               "- _Distance_: {distance} km (Includes {indoor_distance} km of Indoors)\n" \
               "- _Moving Time_: {moving_time} hours (Includes {indoor_moving_time} hours of Indoors)\n" \
               "- _Elevation Gain_: {elevation_gain} km\n" \
               "- _Biggest Run_: {biggest_run} km\n" \
               "- _5's_: {five}\n" \
               "- _10's_: {ten}\n" \
               "- _HM's_: {hm}\n" \
               "- _HM's_: {fm}\n" \
               "- _Ultra's_: {ultra}"

    def all_time_ride_stats(self):
        output_ride_stats = self.output_ride()
        return output_ride_stats.format(
            stats_type="All Time Stats",
            total=self.calculated_stats['ride_at_total'],
            total_indoor=self.calculated_stats['ride_at_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_at_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_at_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['ride_at_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['ride_at_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['ride_at_elevation_gain']),
            biggest_ride=self.operations.meters_to_kilometers(self.calculated_stats['ride_at_biggest_ride']),
            fifties=self.calculated_stats['ride_at_fifty'],
            hundreds=self.calculated_stats['ride_at_hundred'])

    def ytd_ride_stats(self):
        output_ride_stats = self.output_ride()
        return output_ride_stats.format(
            stats_type="Year to Date Stats",
            total=self.calculated_stats['ride_ytd_total'],
            total_indoor=self.calculated_stats['ride_ytd_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_ytd_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_ytd_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['ride_ytd_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['ride_ytd_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['ride_ytd_elevation_gain']),
            biggest_ride=self.operations.meters_to_kilometers(self.calculated_stats['ride_ytd_biggest_ride']),
            fifties=self.calculated_stats['ride_ytd_fifty'],
            hundreds=self.calculated_stats['ride_ytd_hundred'])

    def py_ride_stats(self):
        output_ride_stats = self.output_ride()
        return output_ride_stats.format(
            stats_type="Previous Year Stats",
            total=self.calculated_stats['ride_py_total'],
            total_indoor=self.calculated_stats['ride_py_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_py_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_py_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['ride_py_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['ride_py_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['ride_py_elevation_gain']),
            biggest_ride=self.operations.meters_to_kilometers(self.calculated_stats['ride_py_biggest_ride']),
            fifties=self.calculated_stats['ride_py_fifty'],
            hundreds=self.calculated_stats['ride_py_hundred'])

    def cm_ride_stats(self):
        output_ride_stats = self.output_ride()
        return output_ride_stats.format(
            stats_type="Current Month Stats",
            total=self.calculated_stats['ride_cm_total'],
            total_indoor=self.calculated_stats['ride_cm_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_cm_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_cm_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['ride_cm_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['ride_cm_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['ride_cm_elevation_gain']),
            biggest_ride=self.operations.meters_to_kilometers(self.calculated_stats['ride_cm_biggest_ride']),
            fifties=self.calculated_stats['ride_cm_fifty'],
            hundreds=self.calculated_stats['ride_cm_hundred'])

    def pm_ride_stats(self):
        output_ride_stats = self.output_ride()
        return output_ride_stats.format(
            stats_type="Previous Month Stats",
            total=self.calculated_stats['ride_pm_total'],
            total_indoor=self.calculated_stats['ride_pm_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_pm_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['ride_pm_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['ride_pm_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['ride_pm_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['ride_pm_elevation_gain']),
            biggest_ride=self.operations.meters_to_kilometers(self.calculated_stats['ride_pm_biggest_ride']),
            fifties=self.calculated_stats['ride_pm_fifty'],
            hundreds=self.calculated_stats['ride_pm_hundred'])

    def all_time_run_stats(self):
        output_run_stats = self.output_run()
        return output_run_stats.format(
            stats_type="All Time Stats",
            total=self.calculated_stats['run_at_total'],
            total_indoor=self.calculated_stats['run_at_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['run_at_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['run_at_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['run_at_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['run_at_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['run_at_elevation_gain']),
            biggest_run=self.operations.meters_to_kilometers(self.calculated_stats['run_at_biggest_run']),
            five=self.calculated_stats['run_at_five'],
            ten=self.calculated_stats['run_at_ten'],
            hm=self.calculated_stats['run_at_hm'],
            fm=self.calculated_stats['run_at_fm'],
            ultra=self.calculated_stats['run_at_ultra'])

    def ytd_run_stats(self):
        output_run_stats = self.output_run()
        return output_run_stats.format(
            stats_type="Year to Date Stats",
            total=self.calculated_stats['run_ytd_total'],
            total_indoor=self.calculated_stats['run_ytd_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['run_ytd_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['run_ytd_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['run_ytd_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['run_ytd_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['run_ytd_elevation_gain']),
            biggest_run=self.operations.meters_to_kilometers(self.calculated_stats['run_ytd_biggest_run']),
            five=self.calculated_stats['run_ytd_five'],
            ten=self.calculated_stats['run_ytd_ten'],
            hm=self.calculated_stats['run_ytd_hm'],
            fm=self.calculated_stats['run_ytd_fm'],
            ultra=self.calculated_stats['run_ytd_ultra'])

    def py_run_stats(self):
        output_run_stats = self.output_run()
        return output_run_stats.format(
            stats_type="Previous Year Stats",
            total=self.calculated_stats['run_py_total'],
            total_indoor=self.calculated_stats['run_py_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['run_py_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['run_py_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['run_py_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['run_py_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['run_py_elevation_gain']),
            biggest_run=self.operations.meters_to_kilometers(self.calculated_stats['run_py_biggest_run']),
            five=self.calculated_stats['run_py_five'],
            ten=self.calculated_stats['run_py_ten'],
            hm=self.calculated_stats['run_py_hm'],
            fm=self.calculated_stats['run_py_fm'],
            ultra=self.calculated_stats['run_py_ultra'])

    def cm_run_stats(self):
        output_run_stats = self.output_run()
        return output_run_stats.format(
            stats_type="Current Month Stats",
            total=self.calculated_stats['run_cm_total'],
            total_indoor=self.calculated_stats['run_cm_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['run_cm_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['run_cm_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['run_cm_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['run_cm_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['run_cm_elevation_gain']),
            biggest_run=self.operations.meters_to_kilometers(self.calculated_stats['run_cm_biggest_run']),
            five=self.calculated_stats['run_cm_five'],
            ten=self.calculated_stats['run_cm_ten'],
            hm=self.calculated_stats['run_cm_hm'],
            fm=self.calculated_stats['run_cm_fm'],
            ultra=self.calculated_stats['run_cm_ultra'])

    def pm_run_stats(self):
        output_run_stats = self.output_run()
        return output_run_stats.format(
            stats_type="Previous Month Stats",
            total=self.calculated_stats['run_pm_total'],
            total_indoor=self.calculated_stats['run_pm_indoor_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['run_pm_distance']),
            indoor_distance=self.operations.meters_to_kilometers(self.calculated_stats['run_pm_indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['run_pm_moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['run_pm_indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(self.calculated_stats['run_pm_elevation_gain']),
            biggest_run=self.operations.meters_to_kilometers(self.calculated_stats['run_pm_biggest_run']),
            five=self.calculated_stats['run_pm_five'],
            ten=self.calculated_stats['run_pm_ten'],
            hm=self.calculated_stats['run_pm_hm'],
            fm=self.calculated_stats['run_pm_fm'],
            ultra=self.calculated_stats['run_pm_ultra'])
