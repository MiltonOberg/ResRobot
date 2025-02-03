import streamlit as st
from dashbord_logo import logo
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

    # Skapa en tom plats för loggan längst ner
    placeholder = st.sidebar.empty()
    with placeholder:
        logo()  # Kör loggan


if __name__ == "__main__":
    main()  # Kör huvudfunktionen
