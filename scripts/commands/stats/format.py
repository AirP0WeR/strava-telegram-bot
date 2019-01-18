#  -*- encoding: utf-8 -*-

from common.operations import Operations


class FormatStats(object):

    def __init__(self, calculated_stats):
        self.calculated_stats = calculated_stats
        self.operations = Operations()

    @staticmethod
    def output_ride():
        return "*Ride - {stats_type}:* _(Stats as on: {stats_updated})_\n\n" \
               "- _Rides_: {total} (Includes {total_indoor} Indoors)\n" \
               "- _Distance_: {distance} km (Includes {indoor_distance} km of Indoors)\n" \
               "- _Moving Time_: {moving_time} hours (Includes {indoor_moving_time} hours of Indoors)\n" \
               "- _Elevation Gain_: {elevation_gain} km\n" \
               "- _Biggest Ride_: {biggest_ride} km\n" \
               "- _50's_: {fifties}\n" \
               "- _100's_: {hundreds}"

    @staticmethod
    def output_run():
        return "*Run - {stats_type}:* _(Stats as on: {stats_updated})_\n\n" \
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

    @staticmethod
    def output_swim():
        return "*Swim - {stats_type}:* _(Stats as on: {stats_updated})_\n\n" \
               "- _Swims_: {total}\n" \
               "- _Distance_: {distance} km\n" \
               "- _Moving Time_: {moving_time} hours\n" \
               "- _Biggest Swim_: {biggest_swim} km\n" \
               "- _50 m_: {fifty}\n" \
               "- _100 m_: {hundred}\n" \
               "- _200 m_: {two_hundred}\n" \
               "- _400 m_: {four_hundred}\n" \
               "- _800 m_: {eight_hundred}" \
               "- _1500+ m_: {thousand_five_hundred}"

    def all_time_ride_stats(self):
        output_ride_stats = self.output_ride()
        return output_ride_stats.format(
            stats_type="All Time Stats",
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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
            stats_updated=self.calculated_stats['updated'],
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

    def all_time_swim_stats(self):
        output_swim_stats = self.output_swim()
        return output_swim_stats.format(
            stats_type="All Time Stats",
            stats_updated=self.calculated_stats['updated'],
            total=self.calculated_stats['swim_at_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['swim_at_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['swim_at_moving_time']),
            biggest_swim=self.operations.meters_to_kilometers(self.calculated_stats['swim_at_biggest_ride']),
            fifty=self.calculated_stats['swim_at_50'],
            hundred=self.calculated_stats['swim_at_100'],
            two_hundred=self.calculated_stats['swim_at_200'],
            four_hundred=self.calculated_stats['swim_at_400'],
            eight_hundred=self.calculated_stats['swim_at_800'],
            thousand_five_hundred=self.calculated_stats['swim_at_1500'])

    def ytd_swim_stats(self):
        output_swim_stats = self.output_swim()
        return output_swim_stats.format(
            stats_type="Year to Date Stats",
            stats_updated=self.calculated_stats['updated'],
            total=self.calculated_stats['swim_ytd_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['swim_ytd_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['swim_ytd_moving_time']),
            biggest_swim=self.operations.meters_to_kilometers(self.calculated_stats['swim_ytd_biggest_ride']),
            fifty=self.calculated_stats['swim_ytd_50'],
            hundred=self.calculated_stats['swim_ytd_100'],
            two_hundred=self.calculated_stats['swim_ytd_200'],
            four_hundred=self.calculated_stats['swim_ytd_400'],
            eight_hundred=self.calculated_stats['swim_ytd_800'],
            thousand_five_hundred=self.calculated_stats['swim_ytd_1500'])

    def py_swim_stats(self):
        output_swim_stats = self.output_swim()
        return output_swim_stats.format(
            stats_type="Previous Year Stats",
            stats_updated=self.calculated_stats['updated'],
            total=self.calculated_stats['swim_py_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['swim_py_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['swim_py_moving_time']),
            biggest_swim=self.operations.meters_to_kilometers(self.calculated_stats['swim_py_biggest_ride']),
            fifty=self.calculated_stats['swim_py_50'],
            hundred=self.calculated_stats['swim_py_100'],
            two_hundred=self.calculated_stats['swim_py_200'],
            four_hundred=self.calculated_stats['swim_py_400'],
            eight_hundred=self.calculated_stats['swim_py_800'],
            thousand_five_hundred=self.calculated_stats['swim_py_1500'])

    def cm_swim_stats(self):
        output_swim_stats = self.output_swim()
        return output_swim_stats.format(
            stats_type="Current Month Stats",
            stats_updated=self.calculated_stats['updated'],
            total=self.calculated_stats['swim_cm_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['swim_cm_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['swim_cm_moving_time']),
            biggest_swim=self.operations.meters_to_kilometers(self.calculated_stats['swim_cm_biggest_ride']),
            fifty=self.calculated_stats['swim_cm_50'],
            hundred=self.calculated_stats['swim_cm_100'],
            two_hundred=self.calculated_stats['swim_cm_200'],
            four_hundred=self.calculated_stats['swim_cm_400'],
            eight_hundred=self.calculated_stats['swim_cm_800'],
            thousand_five_hundred=self.calculated_stats['swim_cm_1500'])

    def pm_swim_stats(self):
        output_swim_stats = self.output_swim()
        return output_swim_stats.format(
            stats_type="Previous Month Stats",
            stats_updated=self.calculated_stats['updated'],
            total=self.calculated_stats['swim_pm_total'],
            distance=self.operations.meters_to_kilometers(self.calculated_stats['swim_pm_distance']),
            moving_time=self.operations.seconds_to_human_readable(self.calculated_stats['swim_pm_moving_time']),
            biggest_swim=self.operations.meters_to_kilometers(self.calculated_stats['swim_pm_biggest_ride']),
            fifty=self.calculated_stats['swim_pm_50'],
            hundred=self.calculated_stats['swim_pm_100'],
            two_hundred=self.calculated_stats['swim_pm_200'],
            four_hundred=self.calculated_stats['swim_pm_400'],
            eight_hundred=self.calculated_stats['swim_pm_800'],
            thousand_five_hundred=self.calculated_stats['swim_pm_1500'])
