import streamlit as st
from plot_maps import TripMap
from utils.constants import StationIds


def home():
    st.markdown("# Startsida")


def reseplanerare():
    st.markdown("# Reseplanerare")
    st.markdown(
        "Den här dashboarden syftar till att både utforska data för olika platser, men ska även fungera som en reseplanerare där du får välja och planera din resa."  # noqa: E501
    )


# Remove the hardcoded destination map
# The map is now generated in travel_planner.py based on user input.
""" 
    trip_map = TripMap(
        origin_id=StationIds.MALMO.value, destination_id=StationIds.UMEA.value
    )
    trip_map.display_map()
"""
