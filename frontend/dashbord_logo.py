import streamlit as st


class Dashboard:
    def __init__(self):
        pass

    def logo(self):
        logo_path = "frontend/assets/logo_no_background.png"
        st.image(
            logo_path,
            width=300,  # Adjusted width to fit in a sidebar
        )


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.logo()
