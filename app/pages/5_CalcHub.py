import streamlit as st
import components.sidebar as sidebar

from components.header import render_header

render_header(
    page_title="CalcHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.image("assets/CalcHub.png", width="stretch", output_format="PNG")

st.info(
    "Estamos trabalhando para lançar esta página em breve.",
    icon=":material/construction:",
)
