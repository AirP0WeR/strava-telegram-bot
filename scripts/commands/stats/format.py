#  -*- encoding: utf-8 -*-

from common.operations import Operations


class FormatStats(object):

    def __init__(self, calculated_stats):
        self.calculated_stats = calculated_stats
        self.operations = Operations()

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
               "- _800 m_: {eight_hundred}\n" \
               "- _1500+ m_: {thousand_five_hundred}"

    def ride_stats(self, stats_type, stats_type_key):
        ride_stats = "*Ride - {stats_type}:* _(Stats as on: {stats_updated})_\n\n".format(stats_type=stats_type,
                                                                                          stats_updated=
                                                                                          self.calculated_stats[
                                                                                              'updated'])
        if self.calculated_stats['ride_{}_total'.format(stats_type_key)] > 0:
            ride_stats += "- _Rides_: {total} (Includes {total_indoor} Indoors)\n".format(
                total=self.calculated_stats['ride_{}_total'.format(stats_type_key)],
                total_indoor=self.calculated_stats['ride_{}_indoor_total'.format(stats_type_key)])
            ride_stats += "- _Distance_: {distance} km (Includes {indoor_distance} km of Indoors)\n".format(
                distance=self.operations.meters_to_kilometers(
                    self.calculated_stats['ride_{}_distance'.format(stats_type_key)]),
                indoor_distance=self.operations.meters_to_kilometers(
                    self.calculated_stats['ride_{}_indoor_distance'.format(stats_type_key)]))
            ride_stats += "- _Moving Time_: {moving_time} hours (Includes {indoor_moving_time} hours of Indoors)\n".format(
                moving_time=self.operations.seconds_to_human_readable(
                    self.calculated_stats['ride_{}_moving_time'.format(stats_type_key)]),
                indoor_moving_time=self.operations.seconds_to_human_readable(
                    self.calculated_stats['ride_{}_indoor_moving_time'.format(stats_type_key)]))
            ride_stats += "- _Elevation Gain_: {elevation_gain} km\n".format(
                elevation_gain=self.operations.meters_to_kilometers(
                    self.calculated_stats['ride_{}_elevation_gain'.format(stats_type_key)]))
            ride_stats += "- _Biggest Ride_: {biggest_ride} km\n".format(
                biggest_ride=self.operations.meters_to_kilometers(
                    self.calculated_stats['ride_{}_biggest_ride'.format(stats_type_key)]))
            if self.calculated_stats['ride_{}_fifty'.format(stats_type_key)] > 0:
                ride_stats += "- _50's_: {fifties}\n".format(
                    fifties=self.calculated_stats['ride_{}_fifty'.format(stats_type_key)])
            if self.calculated_stats['ride_{}_hundred'.format(stats_type_key)] > 0:
                ride_stats += "- _100's_: {hundreds}".format(
                    hundreds=self.calculated_stats['ride_{}_hundred'.format(stats_type_key)])
        else:
            ride_stats = "No activities during this period."
            return ride_stats

        return ride_stats

    def run_stats(self, stats_type, stats_type_key):
        output_run_stats = self.output_run()
        return output_run_stats.format(
            stats_type="{stats_type}".format(stats_type=stats_type),
            stats_updated=self.calculated_stats['updated'],
            total=self.calculated_stats['run_{}_total'.format(stats_type_key)],
            total_indoor=self.calculated_stats['run_{}_indoor_total'.format(stats_type_key)],
            distance=self.operations.meters_to_kilometers(
                self.calculated_stats['run_{}_distance'.format(stats_type_key)]),
            indoor_distance=self.operations.meters_to_kilometers(
                self.calculated_stats['run_{}_indoor_distance'.format(stats_type_key)]),
            moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['run_{}_moving_time'.format(stats_type_key)]),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['run_{}_indoor_moving_time'.format(stats_type_key)]),
            elevation_gain=self.operations.meters_to_kilometers(
                self.calculated_stats['run_{}_elevation_gain'.format(stats_type_key)]),
            biggest_run=self.operations.meters_to_kilometers(
                self.calculated_stats['run_{}_biggest_run'.format(stats_type_key)]),
            five=self.calculated_stats['run_{}_five'.format(stats_type_key)],
            ten=self.calculated_stats['run_{}_ten'.format(stats_type_key)],
            hm=self.calculated_stats['run_{}_hm'.format(stats_type_key)],
            fm=self.calculated_stats['run_{}_fm'.format(stats_type_key)],
            ultra=self.calculated_stats['run_{}_ultra'.format(stats_type_key)])

    def swim_stats(self, stats_type, stats_type_key):
        output_swim_stats = self.output_swim()
        return output_swim_stats.format(
            stats_type="{stats_type}".format(stats_type=stats_type),
            stats_updated=self.calculated_stats['updated'],
            total=self.calculated_stats['swim_{}_total'.format(stats_type_key)],
            distance=self.operations.meters_to_kilometers(
                self.calculated_stats['swim_{}_distance'.format(stats_type_key)]),
            moving_time=self.operations.seconds_to_human_readable(
                self.calculated_stats['swim_{}_moving_time'.format(stats_type_key)]),
            biggest_swim=self.operations.meters_to_kilometers(
                self.calculated_stats['swim_{}_biggest_swim'.format(stats_type_key)]),
            fifty=self.calculated_stats['swim_{}_50'.format(stats_type_key)],
            hundred=self.calculated_stats['swim_{}_100'.format(stats_type_key)],
            two_hundred=self.calculated_stats['swim_{}_200'.format(stats_type_key)],
            four_hundred=self.calculated_stats['swim_{}_400'.format(stats_type_key)],
            eight_hundred=self.calculated_stats['swim_{}_800'.format(stats_type_key)],
            thousand_five_hundred=self.calculated_stats['swim_{}_1500'.format(stats_type_key)])
