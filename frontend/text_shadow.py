import streamlit as st


class TextStyler:
    @staticmethod
    def apply_text_shadow():
        st.markdown(
            """
            <style>
            .subheader-text {
                font-size: 1.5em;
                color: white;
                text-shadow: 6px 6px 8px rgba(0, 0, 0, 0.8);
            }
            .title-text {
                font-size: 2em;
                color: white;
                text-shadow: 6px 6px 8px rgba(0, 0, 0, 0.8);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


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


if __name__ == "__main__":
    home()
