import streamlit as st
from plot_maps import TripMap

from backend.connect_to_api import ResRobot
from frontend.trip_planer_visuals import TripPlannerFrontEnd

resrobot = ResRobot()


def reseplanerare():
    st.markdown("# Reseplanerare")
    st.markdown(
        "Den här dashboarden syftar till att både utforska data för olika platser, men ska även fungera som en reseplanerare där du får välja och planera din resa."  # noqa: E501
    )
    try:
        depart_station = st.text_input("Vilken station vill du åka ifrån?: ")
        destination_station = st.text_input("Vart vill du åka?: ")
    except Exception as err:
        st.markdown(f"Skriv in båda alternativen: {err}.")

    if depart_station and destination_station:
        try:
            origin_id = resrobot.return_id(depart_station)
            destination_id = resrobot.return_id(destination_station)
        except Exception as err:
            st.markdown(f"Kunde inte hämta ID: {err}")

        trip_map = TripMap(origin_id=origin_id, destination_id=destination_id)
        trip_map.display_map()

        trip_visuals = TripPlannerFrontEnd(origin_id, destination_id)

        st.markdown(f"## 📍 Din resa: {depart_station} - {destination_station}.")
        st.dataframe(
            trip_visuals.summary_df(), use_container_width=True, hide_index=True
        )

        st.markdown("## 🛑 Lista över alla stopp")

        st.dataframe(
            trip_visuals.get_trip_table(), use_container_width=True, height=500
        )
