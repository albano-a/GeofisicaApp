import qrcode.constants
import streamlit as st
from components.header import render_header
from components.toolshub import qrcode_tab
from components.toolshub.draw_tab import render_draw
import random
import pandas as pd
import qrcode
import io

render_header(
    page_title="SorteioHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.title("Tools")

tools_tab = st.tabs(["QR Code Generator", "Draw"])

with tools_tab[0]:
    qrcode_tab.render_qrcode()

with tools_tab[1]:
    render_draw()
