from stravalib.client import Client


class Hundreds():
    def __init__(self, token):
        self.strava_client = Client()
        self.strava_client.access_token = token

    def main(self):
        messages = []
        no_of_hundreds = "*100 km Rides:*\n\n"
        activities = self.strava_client.get_activities(after="1970-01-01T00:00:00Z")
        count = 0
        for activity in activities:
            if activity.type == "Ride" or activity.type == "VirtualRide":
                if float(activity.distance) >= 100000:
                    count += 1
                    no_of_hundreds += "{}. ".format(count) + "[{}](https://www.strava.com/activities/{})".format(
                        activity.name, activity.id) + " ({})\n".format(activity.start_date_local.date())
                    if count % 25 == 0:
                        messages.append(no_of_hundreds)
                        no_of_hundreds = ""

        messages.append(no_of_hundreds)

        return messages
