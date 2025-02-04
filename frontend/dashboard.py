import streamlit as st
from dashbord_logo import Dashboard
from pages_dict import page_option

from utils.load_css import load_css

load_css("frontend/styles.css")  # Load CSS path using utils/load_css.py


def main():
    """Hanterar sidnavigering i dashboarden"""
    st.sidebar.title("🚀 Navigation")
    page = st.sidebar.radio(
        "# Välj en sida:", list(page_option.keys())
    )  # Lägg till sidopanel
    page_option[page]()  # Kör funktionen kopplad till den valda sidan

    # Skapa en plats för loggan längst ner på sidbar
    st.sidebar.markdown("---")  # Separator
    dashboard = Dashboard()
    with st.sidebar:
        dashboard.logo()  # Ensure the logo is placed in the sidebar


if __name__ == "__main__":
    main()  # Kör huvudfunktionen
