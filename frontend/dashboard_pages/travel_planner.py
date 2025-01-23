import streamlit as st
from backend.connect_to_api import ResRobot
from backend.trips import TripPlanner
from plot_maps import TripMap

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
                trip_planner = TripPlanner(
                    origin_id=origin_id, destination_id=destination_id
                )
                st.markdown(f"Antal stopp: {len(trip_planner.next_available_trip())}")
                st.markdown(f"Tid: {trip_planner.travel_time()}")

        except Exception as err:
            st.markdown(f"Skriv in båda alternativen: {err}.")
