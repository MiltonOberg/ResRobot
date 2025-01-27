from frontend.pages_dict import page_option
import streamlit as st
import pathlib

# CSS för att sätta bakgrundsbild
st.markdown(
    """
    <style>
    .stApp {
        background-image: url(
            https://www.saramellgren.com/wp-content/uploads/2025/01/DALL%C2%B7E-2025-01-27-10.53.05-A-futuristic-illustration-set-in-Goteborg-Sweden-focusing-on-Karlatornet-the-iconic-skyscraper.-The-scene-is-illuminated-by-glowing-neon-blue-and-b-1024x585.webp);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
import streamlit as st
import pathlib


# Function to load CSS from the 'frontend' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("frontend/styles.css")
load_css(css_path)

st.markdown(
    """
    <style>
    .title-text {
        font-size: 2em;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px black;
    }
    .subheader-text {
        font-size: 1.5em;
        color: white;
        text-shadow: 2px 2px 4px black;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="title-text">✨ Welcome to our Travel Robot Dashboard ✨</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader-text">Your complete travel guide 🚆 🚋 🚌</h2>', unsafe_allow_html=True)



st.divider()

# Styled Button
st.button("Click here to plan your next trip!", key="pulse")
st.button("I'm a green button", key="magenta", help="This button is magenta")
if st.button("Click here to plan your next trip!", key="pulse"):
    st.query_params(page_option = "reseplanerare")

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
    st.sidebar.markdown("Select a page to view:")
    st.sidebar.markdown("---")
    st.sidebar.radio("Go to", list(page_option.keys()))


# Skapar en connection till databasen
def main():
    layout()  # Visa huvudlayouten
    page = st.sidebar.radio("# Sidor", page_option.keys())  # Lägg till sidopanel
    page_option[page]()  # Kör funktionen kopplad till den valda sidan


if __name__ == "__main__":
    main()  # Kör huvudfunktionen
