import pathlib
import streamlit as st


def load_css(file_path):
    """Laddar CSS från en extern fil, om filen existerar"""
    css_path = pathlib.Path(file_path)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        print(f"CSS-filen {file_path} hittades inte!")
