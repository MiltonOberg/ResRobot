import streamlit as st


def logo():
    st.markdown(
        """
        <style>
        .stApp.logo-black:before {
            content: url(https://www.saramellgren.com/wp-content/uploads/2025/02/svart-bakrund-1024x1024.png);
            position: fixed;
            top: 0;
            left: 0;
            width: 100px;
            height: 100px;
            z-index: 1000;
            margin: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    logo()
    st.sidebar.title("🚀 Navigation")
