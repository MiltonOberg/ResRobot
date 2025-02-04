import pandas as pd

from backend.trip_details import TripDetails


class TripPlannerFrontEnd(TripDetails):
    def __init__(self, origin_id: int, destination_id: int):
        super().__init__(origin_id, destination_id)

    def get_trip_table(self):
        stops_df = self.next_available_trip()
        stops_df["arrTime"] = stops_df["arrTime"].fillna("-")
        stops_df["depTime"] = stops_df["depTime"].fillna("-")

        stops_df_display = stops_df[
            [
                "name",
                "depTime",
                "arrTime",
            ]
        ].rename(
            columns={
                "name": "🚉Station",
                "depTime": "🚀Avgång",
                "arrTime": "⏳Ankomst",
            }
        )

        stops_df_display = stops_df_display.reset_index(drop=True)  # Reset index
        stops_df_display.index = stops_df_display.index + 1  # Add +1 to index

        return stops_df_display

    def summary_df(self):
        summary_data = {
            "Kategori": ["Antal stopp", "Restid", "Antal byten"],
            "Värde": [
                self.number_stops,
                self.travel_time,
                self.changeovers,
            ],
        }

        return pd.DataFrame(summary_data, dtype=str)
