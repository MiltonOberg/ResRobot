import streamlit as st


def home():
    st.markdown('<div class="start-container">', unsafe_allow_html=True)
    st.markdown(
        '<h2 class="title-text">✨Welcome to our Travel Robot✨</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="loremipsum-text">Vivamus vel sollicitudin risus. Cras vel quam rhoncus, efficitur tellus a, luctus diam. Curabitur efficitur odio diam, lobortis pharetra purus tempor eu. Fusce id semper nibh, at congue orci. Vestibulum non efficitur lacus, id suscipit nunc. Nulla imperdiet mattis feugiat. Pellentesque elit nisi, vestibulum nec risus quis, ornare congue ligula. Quisque sollicitudin arcu non ipsum bibendum interdum. Morbi non porttitor nunc, vel ultrices ligula. Suspendisse potenti. Aenean placerat ligula dolor, sit amet molestie est ultricies sed. Vivamus enim lorem, mattis ut rhoncus in, pretium eget dui. Quisque dictum enim nec turpis pretium sollicitudin. </p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
