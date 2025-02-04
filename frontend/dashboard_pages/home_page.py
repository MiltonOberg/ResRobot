import streamlit as st

from frontend.text_shadow import TextStyler


def home():
    TextStyler.apply_text_shadow()
    st.markdown(
        '<h1 class="title-text">✨ Welcome to SKAM Travel Robot Dashboard ✨</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h2 class="subheader-text">Your complete travel guide 🚆 🚋 🚌</h2>',
        unsafe_allow_html=True,
    )
