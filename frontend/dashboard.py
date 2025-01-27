from frontend.pages_dict import page_option
import streamlit as st

# CSS för att sätta bakgrundsbild
st.markdown(
    """
    <style>
    .stApp {
        background-image: url(
            "https://www.saramellgren.com/wp-content/uploads/2023/11/saram0214_an_astronaut_playing_with_jellyfish_fa601ffe-ecda-4a23-9977-f958ecb739e4-1.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def layout():
    st.title("Welcome to our Travel Robot Dashboard")
    st.markdown("Your complete travel guide")
    st.markdown("---")


# Skapar en connection till databasen
def main():
    layout()  # Visa huvudlayouten
    page = st.sidebar.radio("# Sidor", page_option.keys())  # Lägg till sidopanel
    page_option[page]()  # Kör funktionen kopplad till den valda sidan


if __name__ == "__main__":
    main()  # Kör huvudfunktionen
