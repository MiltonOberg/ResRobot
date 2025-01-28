from datetime import datetime, timedelta

import pandas as pd

from backend.connect_to_api import ResRobot

resrobot = ResRobot()


class TripPlanner:
    """
    A class to interact with Resrobot API to plan trips and retrieve details of available journeys.

    Check explorations to find id for your location

    Attributes:
    ----------
    trips : list
        A list of trips retrieved from the Resrobot API for the specified origin and destination.
    number_trips : int
        The total number of trips available for the specified origin and destination.

    Methods:
    -------
    next_available_trip() -> pd.DataFrame:
        Returns a DataFrame containing details of the next available trip, including stop names,
        coordinates, departure and arrival times, and dates.
    next_available_trips_today() -> list[pd.DataFrame]
        Returns a list of DataFrame objects, where each DataFrame contains similar content as next_available_trip()
    """

    def __init__(self, origin_id, destination_id) -> None:
        self.trips = resrobot.trips(origin_id, destination_id).get("Trip")
        self.number_trips = len(self.trips)

    def next_available_trip(self) -> pd.DataFrame:
        next_trip = self.trips[0]

        leglist = next_trip.get("LegList").get("Leg")

        df_legs = pd.DataFrame(leglist)

        df_stops = pd.json_normalize(df_legs["Stops"].dropna(), "Stop", errors="ignore")

        df_stops["time"] = df_stops["arrTime"].fillna(df_stops["depTime"])
        df_stops["date"] = df_stops["arrDate"].fillna(df_stops["depDate"])

        return df_stops[
            [
                "name",
                "extId",
                "lon",
                "lat",
                "depTime",
                "depDate",
                "arrTime",
                "arrDate",
                "time",
                "date",
            ]
        ]

    def travel_time(self):
        depart_time = self.next_available_trip().iloc[0]["depTime"]
        arrival_time = self.next_available_trip().iloc[-1]["arrTime"]
        time_format = "%H:%M:%S"
        # from string to time object to get the diffrence
        datetime_depart = datetime.strptime(depart_time, time_format)
        datetime_arrival = datetime.strptime(arrival_time, time_format)
        # diffrence
        travel_time = datetime_arrival - datetime_depart

        time = []
        for item in str(travel_time).split(":"):
            if "day" in item:
                time.append(int(item.split("day, ")[0]) * -1)
                time.append(item.split("day, ")[-1])
            else:
                time.append(item)
        # remove seconds
        time.remove(time[-1])

        return (
            "{} timmar {} minuter".format(*time)
            if len(time) == 2
            else "{} dag {} timmar {} minuter".format(*time)
        )

    def changeovers(self):
        next_trip = self.trips[0]
        stops = next_trip["LegList"]["Leg"]
        filtered_names = [
            stops[i]["name"]
            for i in range(len(stops))
            if stops[i]["name"] != "Byten" or stops[i]["name"] == "Promenad"
        ]
        number_change_overs = sum(
            [
                (1 if filtered_names[i] not in filtered_names[i - 1] else 0)
                for i in range(len(filtered_names))
            ]
        )
        return number_change_overs

    def next_available_trips_today(self) -> list[pd.DataFrame]:
        """Fetches all available trips today between the origin_id and destination_id
        It returns a list of DataFrame objects, where each item corresponds to a trip
        """
        today = datetime.now().date()
        trips_today = []

        for trip in self.trips:
            leglist = trip.get("LegList").get("Leg")
            df_legs = pd.DataFrame(leglist)
            df_stops = pd.json_normalize(
                df_legs["Stops"].dropna(), "Stop", errors="ignore"
            )
            df_stops["depDate"] = pd.to_datetime(df_stops["depDate"]).dt.date
            if df_stops["depDate"].iloc[0] == today:
                trips_today.append(df_stops)

        return trips_today

    def choose_time_departure(self, hours: int = 0, minutes: int = 0):
        time_format = "%H:%M:%S"
        current_time = datetime.now()
        current_time_delta = timedelta(
            hours=current_time.hour, minutes=current_time.minute
        )
        trips_list = []
        departure = timedelta(hours=hours, minutes=minutes)
        for trip in self.trips:
            legs = trip.get("LegList").get("Leg")
            for leg in legs:
                if "Stops" in leg:
                    stops = leg["Stops"]["Stop"]
                    dep_time = datetime.strptime(stops[0]["depTime"], time_format)
                    dep_time_delta = timedelta(
                        hours=int(dep_time.hour), minutes=int(dep_time.minute)
                    )
                    if dep_time_delta >= abs(departure + current_time_delta):
                        trips_list.append(trip)

        return trips_list


# Slut på trips.py
