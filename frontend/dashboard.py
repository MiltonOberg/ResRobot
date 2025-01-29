import pathlib

import streamlit as st

from frontend.pages_dict import page_option


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

# Styled Button
st.button("Click here to plan your next trip!", key="pulse")


# Text Input with Custom Font and Color
st.header("Styled Text Input")
st.text_input("Enter your favorite quote:", key="styledinput")


# Text Area with Custom Font
st.header("Styled Text Area")
st.text_area("Your thoughts:", key="styledtextarea")

# Radio Buttons with Custom Styles
st.header("Styled Radio Buttons")
st.radio("Pick a choice:", ["Choice A", "Choice B", "Choice C"], key="styledradio")

# Markdown with Custom Font and Color
st.header("Styled Markdown")
st.markdown(
    '<p class="custom-markdown">This is <strong>bold text</strong> with a custom font and color.</p>',
    unsafe_allow_html=True,
)


def layout():
    st.sidebar.title("🚀 Navigation")
    st.sidebar.radio("Go to", list(page_option.keys()))


# Skapar en connection till databasen
def main():
    layout()  # Visa huvudlayouten
    page = st.sidebar.radio("# Sidor", page_option.keys())  # Lägg till sidopanel
    page_option[page]()  # Kör funktionen kopplad till den valda sidan


if __name__ == "__main__":
    main()  # Kör huvudfunktionen
