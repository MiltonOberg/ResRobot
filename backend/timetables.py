import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


class Tables:
    API_KEY = os.getenv("API_KEY")

    def access_id_from_location(self, location):
        url = f"https://api.resrobot.se/v2.1/location.name?input={location}&format=json&accessId={self.API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching location data: {e}")
            return []

        result = response.json()
        location_options = []

        stops = result.get("stopLocationOrCoordLocation", [])
        for stop in stops:
            for key, stop_data in stop.items():
                name = stop_data.get("name")
                extId = stop_data.get("extId")
                if name and extId:
                    location_options.append({"name": name, "extId": extId})

        return location_options

    def return_id(self, location):
        url = f"https://api.resrobot.se/v2.1/location.name?input={location}&format=json&accessId={self.API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            stops = result.get("stopLocationOrCoordLocation", [])

            if stops:
                stop_data = next(iter(stops[0].values()))
                return stop_data.get("extId", None)
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching location ID: {e}")
            return None

    def departures(self, location_id):
        url = f"https://api.resrobot.se/v2.1/departureBoard?id={location_id}&format=json&accessId={self.API_KEY}"
        response = requests.get(url)
        data = response.json()
        departures = data.get("Departure", [])

        departure_list = []
        for dep in departures:
            line = dep["ProductAtStop"]["line"]
            direction = dep["direction"]
            stop = dep["stop"]
            time = dep["time"]
            date = dep["date"]
            departure_list.append(
                {
                    "Date": date,
                    "Time": time,
                    "Line": line,
                    "Direction": direction,
                    "Stop": stop,
                }
            )

        df = pd.DataFrame(departure_list)

        if departures:
            # stop_name = departures[0]["stop"]
            date_str = departures[0]["date"]
        else:
            # stop_name = "Unknown Stop"
            date_str = "Unknown Date"

        now = datetime.now()
        df["Departures in"] = df["Time"].apply(
            lambda t: (
                datetime.strptime(f"{date_str} {t}", "%Y-%m-%d %H:%M:%S") - now
            ).total_seconds()
            // 60
        )
        df["Departures in"] = df["Departures in"].apply(
            lambda m: (
                "now"
                if m == 0
                else (
                    f"{int(m // 60)} h {int(m % 60)} min"
                    if m >= 60
                    else f"{int(m)} min"
                )
            )
        )

        df_departures = df[["Line", "Direction", "Departures in"]].reset_index(
            drop=True
        )
        return df_departures

    def arrivals(self, location_id):
        url = f"https://api.resrobot.se/v2.1/arrivalBoard?id={location_id}&format=json&accessId={self.API_KEY}"
        response = requests.get(url)
        data = response.json()
        arrivals = data.get("Arrival", [])

        arrival_list = []
        for arr in arrivals:
            line = arr["ProductAtStop"]["line"]
            origin = arr["origin"]
            stop = arr["stop"]
            time = arr["time"]
            date = arr["date"]
            arrival_list.append(
                {
                    "Date": date,
                    "Time": time,
                    "Line": line,
                    "Origin": origin,
                    "Stop": stop,
                }
            )

        df = pd.DataFrame(arrival_list)

        if arrivals:
            date_str = arrivals[0]["date"]
        else:
            date_str = "Unknown Date"

        now = datetime.now()
        df["Arrives in"] = df["Time"].apply(
            lambda t: (
                datetime.strptime(f"{date_str} {t}", "%Y-%m-%d %H:%M:%S") - now
            ).total_seconds()
            // 60
        )
        df["Arrives in"] = df["Arrives in"].apply(
            lambda m: (
                "now"
                if m == 0
                else (
                    f"{int(m // 60)} h {int(m % 60)} min"
                    if m >= 60
                    else f"{int(m)} min"
                )
            )
        )

        df = df[["Line", "Origin", "Arrives in"]].reset_index(drop=True)
        return df


if __name__ == "__main__":
    tables = Tables()
    df = tables.arrivals(location_id="740000001")
    print(df)
