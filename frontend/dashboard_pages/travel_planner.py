import pandas as pd
import streamlit as st
from plot_maps import TripMap

from backend.connect_to_api import ResRobot
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from backend.trips import TripPlanner
import pandas as pd
=======
from backend.trip_details import TripDetails
=======
from backend.trips import TripPlanner
>>>>>>> b56e7c1 (removed changes in travel planner page)
from frontend.plot_maps import TripMap
>>>>>>> ac1bd6d (lagt till en ny klass för att dela upp tripplanner. Nu finns en trip details, där små detaljer om valda resan går att hämta)
=======
from backend.trip_details import TripDetails
from backend.trips import TripPlanner
>>>>>>> d9d5b5c (fix with refactor implementaions)

resrobot = ResRobot()


def reseplanerare():
    st.markdown("# Reseplanerare")
    st.markdown(
        "Den här dashboarden syftar till att både utforska data för olika platser, men ska även fungera som en reseplanerare där du får välja och planera din resa."  # noqa: E501
    )

    depart_station = st.text_input("Vilken station vill du åka ifrån?: ")
    destination_station = st.text_input("Vart vill du åka?: ")

    if depart_station and depart_station:
        try:
            origin_id = resrobot.return_id(depart_station)
            destination_id = resrobot.return_id(destination_station)

            col1, col2 = st.columns([4, 1], gap="small")

            with col1:
                trip_map = TripMap(origin_id=origin_id, destination_id=destination_id)
                trip_map.display_map()

            with col2:
                trip_details = TripDetails(
                    origin_id=origin_id, destination_id=destination_id
                )
                trip_planner = TripPlanner(
                    origin_id=origin_id, destination_id=destination_id
                )
<<<<<<< HEAD
<<<<<<< HEAD

            summary_data = {
                "Kategori": ["Antal stopp", "Restid", "Antal byten"],
                "Värde": [
                    trip_details.number_stops,
                    trip_details.travel_time,
                    trip_details.changeovers,
                ],
            }

            """
            print(trip_planner.next_available_trip().iloc[0]["depTime"],)
            print(trip_planner.next_available_trip().iloc[-1]["arrTime"],
            )
            """

            summary_df = pd.DataFrame(summary_data, dtype=str)

            st.markdown(f"## 📍 Din resa: {depart_station} - {destination_station}.")
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

            stops_df = trip_planner.next_available_trip().copy()

            stops_df.loc[stops_df["arrTime"].isna(), "arrTime"] = " - "
            stops_df.loc[stops_df["depTime"].isna(), "depTime"] = " - "

            st.markdown("## 🛑 Lista över alla stopp")
            stops_df_display = stops_df[["name", "arrTime", "depTime"]].rename(
                columns={
                    "name": "🚉Station",
                    "arrTime": "⏳Ankomst",
                    "depTime": "🚀Avgång",
                }
            )

            stops_df_display = stops_df_display.reset_index(drop=True)  # Reset index
            stops_df_display.index = stops_df_display.index + 1  # Add +1 to index

            st.dataframe(stops_df_display, use_container_width=True, height=500)
=======
                st.markdown(f"Tid: {trip_details.travel_time}")
                st.markdown(f"Antal stopp: {trip_details.number_stops}")
                st.markdown(f"Byten: {trip_details.changeovers}")
>>>>>>> ac1bd6d (lagt till en ny klass för att dela upp tripplanner. Nu finns en trip details, där små detaljer om valda resan går att hämta)
=======
                st.markdown(f"Antal stopp: {len(trip_planner.next_available_trip())}")
                st.markdown(f"Tid: {trip_planner.travel_time()}")
                st.markdown(f"Antal byten: {trip_planner.changeovers()}")
>>>>>>> b56e7c1 (removed changes in travel planner page)

        except Exception as err:
            st.markdown(f"Skriv in båda alternativen: {err}.")
