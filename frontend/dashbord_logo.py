import streamlit as st


class Dashboard:
    def __init__(self):
        pass

    def logo(self):
        st.image(
            "https://www.saramellgren.com/wp-content/uploads/2025/02/svart-bakrund-1.png",
            width=300,  # Adjusted width to fit in a sidebar
        )


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.logo()
