import streamlit as st


def show():
    st.sidebar.image("assets/GeofisicaApp.svg", use_container_width=True)
    st.sidebar.link_button("Retornar ao GeofisicaHub", url="https://geofisicahub.me/", icon=":material/arrow_back:" ,type="primary")
