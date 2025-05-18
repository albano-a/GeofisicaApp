import streamlit as st
import numpy as np
from components.seishub.wavelet_tab import render_wavelet
from components.header import render_header

render_header(
    page_title="SeisHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.header("SeisHub")

_tabs = ["Wavelets"]

tabs = st.tabs(_tabs)

with tabs[0]:
    render_wavelet()
