#  -*- encoding: utf-8 -*-

from common.operations import Operations


class FormatStats(object):

    def __init__(self, calculated_stats):
        self.calculated_stats = calculated_stats
        self.operations = Operations()

    def ride_stats(self, stats_type, stats_type_key):
        ride_stats = "*Ride - {stats_type}:* _(Stats as on: {stats_updated})_\n\n".format(stats_type=stats_type,
                                                                                          stats_updated=
                                                                                          self.calculated_stats[
                                                                                              'updated'])
        if self.calculated_stats['ride_{}_total'.format(stats_type_key)] > 0:
            ride_stats += "- _Rides_: {total} ".format(
                total=self.calculated_stats['ride_{}_total'.format(stats_type_key)])
            if self.calculated_stats['ride_{}_indoor_total'.format(stats_type_key)] > 0:
                ride_stats += "(Includes {total_indoor} Indoors)\n".format(
                    total_indoor=self.calculated_stats['ride_{}_indoor_total'.format(stats_type_key)])
            else:
                ride_stats += "\n"

            ride_stats += "- _Distance_: {distance} km ".format(distance=self.operations.meters_to_kilometers(
                self.calculated_stats['ride_{}_distance'.format(stats_type_key)]))
            if self.calculated_stats['ride_{}_indoor_distance'.format(stats_type_key)] > 0:
                ride_stats += "(Includes {indoor_distance} km of Indoors)\n".format(
                    indoor_distance=self.operations.meters_to_kilometers(
                        self.calculated_stats['ride_{}_indoor_distance'.format(stats_type_key)]))
            else:
                ride_stats += "\n"

            ride_stats += "- _Moving Time_: {moving_time} hours ".format(
                moving_time=self.operations.seconds_to_human_readable(
                    self.calculated_stats['ride_{}_moving_time'.format(stats_type_key)]))
            if self.calculated_stats['ride_{}_indoor_moving_time'.format(stats_type_key)] > 0:
                ride_stats += "(Includes {indoor_moving_time} hours of Indoors)\n".format(
                    indoor_moving_time=self.operations.seconds_to_human_readable(
                        self.calculated_stats['ride_{}_indoor_moving_time'.format(stats_type_key)]))
            else:
                ride_stats += "\n"

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
            ride_stats = "No activities found during this period."
            return ride_stats

        return ride_stats

    def run_stats(self, stats_type, stats_type_key):
        run_stats = "*Run - {stats_type}:* _(Stats as on: {stats_updated})_\n\n".format(
            stats_type="{stats_type}".format(stats_type=stats_type), stats_updated=self.calculated_stats['updated'])
        if self.calculated_stats['run_{}_total'.format(stats_type_key)] > 0:
            run_stats += "- _Runs_: {total} ".format(total=self.calculated_stats['run_{}_total'.format(stats_type_key)])
            if self.calculated_stats['run_{}_indoor_total'.format(stats_type_key)] > 0:
                run_stats += "(Includes {total_indoor} Indoors)\n".format(
                    total_indoor=self.calculated_stats['run_{}_indoor_total'.format(stats_type_key)])
            else:
                run_stats += "\n"

            run_stats += "- _Distance_: {distance} km ".format(distance=self.operations.meters_to_kilometers(
                self.calculated_stats['run_{}_distance'.format(stats_type_key)]))
            if self.calculated_stats['run_{}_indoor_distance'.format(stats_type_key)] > 0:
                run_stats += "(Includes {indoor_distance} km of Indoors)\n".format(
                    indoor_distance=self.operations.meters_to_kilometers(
                        self.calculated_stats['run_{}_indoor_distance'.format(stats_type_key)]))
            else:
                run_stats += "\n"

            run_stats += "- _Moving Time_: {moving_time} hours ".format(
                moving_time=self.operations.seconds_to_human_readable(
                    self.calculated_stats['run_{}_moving_time'.format(stats_type_key)]))
            if self.calculated_stats['run_{}_indoor_moving_time'.format(stats_type_key)] > 0:
                run_stats += "(Includes {indoor_moving_time} hours of Indoors)\n".format(
                    indoor_moving_time=self.operations.seconds_to_human_readable(
                        self.calculated_stats['run_{}_indoor_moving_time'.format(stats_type_key)]))
            else:
                run_stats += "\n"

            run_stats += "- _Elevation Gain_: {elevation_gain} km\n".format(
                elevation_gain=self.operations.meters_to_kilometers(
                    self.calculated_stats['run_{}_elevation_gain'.format(stats_type_key)]))
            run_stats += "- _Biggest Run_: {biggest_run} km\n".format(
                biggest_run=self.operations.meters_to_kilometers(
                    self.calculated_stats['run_{}_biggest_run'.format(stats_type_key)]))
            if self.calculated_stats['run_{}_five'.format(stats_type_key)] > 0:
                run_stats += "- _5's_: {five}\n".format(
                    five=self.calculated_stats['run_{}_five'.format(stats_type_key)])
            if self.calculated_stats['run_{}_ten'.format(stats_type_key)] > 0:
                run_stats += "- _10's_: {ten}\n".format(
                    ten=self.calculated_stats['run_{}_ten'.format(stats_type_key)])
            if self.calculated_stats['run_{}_hm'.format(stats_type_key)] > 0:
                run_stats += "- _HM's_: {hm}\n".format(hm=self.calculated_stats['run_{}_hm'.format(stats_type_key)])
            if self.calculated_stats['run_{}_fm'.format(stats_type_key)] > 0:
                run_stats += "- _FM's_: {fm}\n".format(fm=self.calculated_stats['run_{}_fm'.format(stats_type_key)])
            if self.calculated_stats['run_{}_ultra'.format(stats_type_key)] > 0:
                run_stats += "- _Ultra's_: {ultra}".format(
                    ultra=self.calculated_stats['run_{}_ultra'.format(stats_type_key)])
        else:
            run_stats = "No activities found during this period."
            return run_stats

        return run_stats

    def swim_stats(self, stats_type, stats_type_key):
        swim_stats = "*Swim - {stats_type}:* _(Stats as on: {stats_updated})_\n\n".format(
            stats_type="{stats_type}".format(stats_type=stats_type), stats_updated=self.calculated_stats['updated'])
        if self.calculated_stats['swim_{}_total'.format(stats_type_key)] > 0:
            swim_stats += "- _Swims_: {total}\n".format(
                total=self.calculated_stats['swim_{}_total'.format(stats_type_key)])
            swim_stats += "- _Distance_: {distance} km\n".format(distance=self.operations.meters_to_kilometers(
                self.calculated_stats['swim_{}_distance'.format(stats_type_key)]))
            swim_stats += "- _Moving Time_: {moving_time} hours\n".format(
                moving_time=self.operations.seconds_to_human_readable(
                    self.calculated_stats['swim_{}_moving_time'.format(stats_type_key)]))
            swim_stats += "- _Biggest Swim_: {biggest_swim} km\n".format(
                biggest_swim=self.operations.meters_to_kilometers(
                    self.calculated_stats['swim_{}_biggest_swim'.format(stats_type_key)]))
            if self.calculated_stats['swim_{}_50'.format(stats_type_key)] > 0:
                swim_stats += "- _50 m_: {fifty}\n".format(
                    fifty=self.calculated_stats['swim_{}_50'.format(stats_type_key)])
            if self.calculated_stats['swim_{}_100'.format(stats_type_key)] > 0:
                swim_stats += "- _100 m_: {hundred}\n".format(
                    hundred=self.calculated_stats['swim_{}_100'.format(stats_type_key)])
            if self.calculated_stats['swim_{}_200'.format(stats_type_key)] > 0:
                swim_stats += "- _200 m_: {two_hundred}\n".format(
                    two_hundred=self.calculated_stats['swim_{}_200'.format(stats_type_key)])
            if self.calculated_stats['swim_{}_400'.format(stats_type_key)] > 0:
                swim_stats += "- _400 m_: {four_hundred}\n".format(
                    four_hundred=self.calculated_stats['swim_{}_400'.format(stats_type_key)])
            if self.calculated_stats['swim_{}_800'.format(stats_type_key)] > 0:
                swim_stats += "- _800 m_: {eight_hundred}\n".format(
                    eight_hundred=self.calculated_stats['swim_{}_800'.format(stats_type_key)])
            if self.calculated_stats['swim_{}_1500'.format(stats_type_key)] > 0:
                swim_stats += "- _1500+ m_: {thousand_five_hundred}".format(
                    thousand_five_hundred=self.calculated_stats['swim_{}_1500'.format(stats_type_key)])
        else:
            swim_stats = "No activities found during this period."
            return swim_stats

        return swim_stats
