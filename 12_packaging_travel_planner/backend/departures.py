from trips import TripPlanner
from connect_to_api import ResRobot
import pandas as pd
import requests

resrobot = ResRobot()
origin_id = input("Enter your location: ")
destination_id = input("Enter your destination: ")  
 
class DepaturePlanner(TripPlanner):
    
    def __init__(self, origin_id, destination_id):
        super().__init__(origin_id, destination_id)
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.trips = resrobot.trips(self.origin_id, self.destination)
                  
    def next_available_trip(self) -> pd.DataFrame:
        next_trip = self.trips[0]
        return next_trip
       
    def timetable_departure(self, location_id):
        url = f"https://api.resrobot.se/v2.1/departureBoard?id={location_id}&format=json&accessId={self.API_KEY}"
        location_id = origin_id
        response = requests.get(url)
        result = response.json()
        return result

    def timetable_arrival(self, location_id):
        url = f"https://api.resrobot.se/v2.1/arrivalBoard?id={location_id}&format=json&accessId={self.API_KEY}"
        location_id = destination_id
        response = requests.get(url)
        result = response.json()
        return result
