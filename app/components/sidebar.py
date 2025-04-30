import streamlit as st


def show():
    st.sidebar.image("assets/GeofisicaApp.svg", use_container_width=True)
    st.link_button("Retornar ao GeofisicaHub", url="https://geofisicahub.me/")
