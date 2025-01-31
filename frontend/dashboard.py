import pathlib

import streamlit as st
from pages_dict import page_option


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("frontend/styles.css")
load_css(css_path)
()

st.markdown(
    '<h1 class="title-text">✨ Welcome to our Travel Robot Dashboard ✨</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<h2 class="subheader-text">Your complete travel guide 🚆 🚋 🚌</h2>',
    unsafe_allow_html=True,
)
st.divider()


# Skapar en connection till databasen
def main():
    page = st.sidebar.radio("# 🚀 Navigation", page_option.keys())  # Lägg till sidopanel
    page_option[page]()  # Kör funktionen kopplad till den valda sidan


if __name__ == "__main__":
    main()  # Kör huvudfunktionen
