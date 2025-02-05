import streamlit as st


def home():
    st.markdown('<div class="start-container">', unsafe_allow_html=True)
    st.markdown(
        '<h2 class="title-text">✨Welcome to our Travel Robot✨</h2>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
