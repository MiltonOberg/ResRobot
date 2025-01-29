import requests
from connect_to_api import ResRobot
from trips import TripPlanner


class DepaturePlanner(TripPlanner):
    def __init__(self, origin_id, destination_id):
        super().__init__(origin_id, destination_id)
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.access_id_from_location(self.origin_id)
        self.access_id_from_location(self.destination_id)
        resrobot = ResRobot()
        self.trips = resrobot.trips(self.origin_id, self.destination)

    def access_id_from_location(self, location, start_location):
        url = f"https://api.resrobot.se/v2.1/location.name?input={location}&format=json&accessId={self.API_KEY}"
        start_location = start_location
        response = requests.get(url)
        result = response.json()
        return result  # temp fix

    def timetable_departure(self, location_id, end_location):
        url = f"https://api.resrobot.se/v2.1/departureBoard?id={location_id}&format=json&accessId={self.API_KEY}"
        location_id = self.origin_id
        end_location = end_location
        response = requests.get(url)
        result = response.json()
        return result

    def next_trip(self):
        next_trip = self.trips["Trip"]
        return next_trip

    def Static_data(self):
        url = f"https://opendata.samtrafiken.se/gtfs-sweden/sweden.zip?key={self.API_KEY}."
        response = requests.get(url)
        result = response.json()
        return result
