import streamlit as st


def show():
    st.sidebar.image(
        "assets/GeofisicaApp_beta.png", use_container_width=True, output_format="PNG"
    )
    st.sidebar.link_button(
        "Retornar ao GeofisicaHub",
        url="https://geofisicahub.me/",
        icon=":material/arrow_back:",
        type="primary",
    )
