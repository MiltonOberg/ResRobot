import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


class Tables:
    API_KEY = os.getenv("API_KEY")

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

        df = df[["Line", "Direction", "Departures in"]].reset_index(drop=True)
        return df


if __name__ == "__main__":
    tables = Tables()
    df = tables.departures(location_id="740000001")
    print(df)
