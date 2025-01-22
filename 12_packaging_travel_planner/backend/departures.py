from backend.connect_to_api import ResRobot
from trips import TripPlanner
from connect_to_api import 



resrobot = ResRobot()
origin_id = input("Enter your location: ")
destination_id = input("Enter your destination: ")


class DepaturePlanner(TripPlanner):
    
    resrobot = ResRobot()
    origin_id = input("Enter your location: ")
    destination_id = input("Enter your destination: ")

    def next_available_trip(self) -> pd.DataFrame:
        next_trip = self.trips[0]
        
        
    def timetable_departure(self, location_id):
        location_id = origin_id
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
