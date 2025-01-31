from datetime import datetime, timedelta

from backend.trips import TripPlanner


class TripDetails(TripPlanner):
    """
    Used to get additional details about your chosen trip
    number of stops
    how long the trip is
    number of changeovers
    """

    def __init__(self, origin_id: int, destination_id: int):
        super().__init__(origin_id, destination_id)
        self.number_stops = len(self.next_available_trip())
        self.travel_time = self._travel_time()
        self.changeovers = self._changeovers()

    def _travel_time(self):
        depart_time = self.next_available_trip().iloc[0]["depTime"]
        arrival_time = self.next_available_trip().iloc[-1]["arrTime"]
        time_format = "%H:%M:%S"
        # from string to time object to get the diffrence
        datetime_depart = datetime.strptime(depart_time, time_format)
        datetime_arrival = datetime.strptime(arrival_time, time_format)

        # adapt for 24 hour transition
        if datetime_arrival < datetime_depart:
            datetime_arrival += timedelta(days=+1)

        # diffrence
        travel_time = datetime_arrival - datetime_depart

        total_seconds = travel_time.total_seconds()
        days = int(total_seconds // 86400)
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)

        if days > 0:
            return f"{days} dag {hours} timmar {minutes} minuter"
        return f"{hours} timmar {minutes} minuter"

    def _changeovers(self):
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
