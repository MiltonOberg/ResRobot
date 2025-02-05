import streamlit as st
from dotenv import load_dotenv

from backend.timetables import Tables


def home():
    load_dotenv()

    st.markdown('<div class="start-container">', unsafe_allow_html=True)

    # st.markdown("</div>", unsafe_allow_html=True)

    # st.markdown('<div class="timetable-container">', unsafe_allow_html=True)

    st.title("✨Tidtabellen✨")

    # Get city
    location_name = st.text_input("Ange en stad:", "")

    if location_name:
        resrobot = Tables()
        location_options = resrobot.access_id_from_location(location_name)

        if location_options:
            location_dict = {loc["name"]: loc["extId"] for loc in location_options}
            selected_location = st.selectbox(
                "Välj en hållplats:", list(location_dict.keys())
            )
            location_id = location_dict[selected_location]

            if location_id:
                tables = Tables()

                # Choose between Arrivals and Departures
                option = st.radio("Välj tidtabell:", ["Ankomster", "Avgångar"])

                st.subheader(f"{option} Tabell")

                if option == "Ankomster":
                    df_arrivals = tables.arrivals(location_id)
                    st.dataframe(df_arrivals, use_container_width=True, hide_index=True)
                elif option == "Avgångar":
                    df_departures = tables.departures(location_id)
                    st.dataframe(
                        df_departures, use_container_width=True, hide_index=True
                    )
            else:
                st.error("Kunde inte hämta ett giltigt plats-ID. Försök igen.")
        else:
            st.error(
                "Inga matchande platser hittades. Kontrollera stavningen på platsen."
            )
    else:
        st.warning("Ange ett platsnamn för att fortsätta.")

    st.markdown("</div>", unsafe_allow_html=True)
