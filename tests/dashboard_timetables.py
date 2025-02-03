import streamlit as st
from dotenv import load_dotenv

from backend.timetables import Tables

load_dotenv()


def main():
    st.title("Timetables Dashboard")

    # Get location
    location_name = st.text_input("Enter a city:", "")

    if location_name:
        resrobot = Tables()
        location_options = resrobot.access_id_from_location(location_name)

        if location_options:
            location_dict = {loc["name"]: loc["extId"] for loc in location_options}
            selected_location = st.selectbox(
                "Select a stop:", list(location_dict.keys())
            )
            location_id = location_dict[selected_location]

            if location_id:
                st.write(f"Location ID: {location_id}")
                tables = Tables()

                # Choose between Arrivals and Departures
                option = st.radio("Select timetable:", ["Arrivals", "Departures"])

                st.subheader(f"{option} Table")

                if option == "Arrivals":
                    df_arrivals = tables.arrivals(location_id)
                    st.dataframe(df_arrivals, use_container_width=True)
                elif option == "Departures":
                    df_departures = tables.departures(location_id)
                    st.dataframe(df_departures, use_container_width=True)
            else:
                st.error("Could not retrieve a valid location ID. Please try again.")
        else:
            st.error("No matching locations found. Please check the location name.")
    else:
        st.warning("Please enter a location name to proceed.")


if __name__ == "__main__":
    main()
