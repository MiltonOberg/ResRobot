import streamlit as st
from frontend.pages_dict import page_option


def main():
    page = st.sidebar.radio("# Sidor", page_option.keys())
    page_option[page]()


if __name__ == "__main__":
    main()
