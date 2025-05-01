import streamlit as st
import components.sidebar as sidebar

st.set_page_config(
    page_title="FisicaHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

sidebar.show()

st.image("assets/FisicaHub.png", use_container_width=True, output_format="PNG")

st.info(
    "Estamos trabalhando para lançar esta página em breve.",
    icon=":material/construction:",
)