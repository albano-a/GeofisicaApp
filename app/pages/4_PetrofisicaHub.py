import streamlit as st
import components.sidebar as sidebar
import numpy as np
import matplotlib.pyplot as plt

from components.petrofisicahub.porosity_tab import render_porosity
from components.petrofisicahub.permeability_tab import render_permeability
from components.petrofisicahub.resistivity_tab import render_resistivity
from components.petrofisicahub.water_saturation_tab import render_water_saturation
from components.petrofisicahub.shale_volume_tab import render_shale_volume
from components.petrofisicahub.oil_reserves_tab import render_oil_reserves

from components.header import render_header

render_header(
    page_title="PetrofisicaHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.image("assets/PetrofisicaHub.png", width="stretch", output_format="PNG")

st.write(
    "Welcome to PetrofisicaHub! This page contains several equations to calculate porosity, permeability, water saturation and so on."
)

tabs_list = [
    "Porosity",
    "Permeability",
    "Resistivity",
    "Water Saturation",
    "Shale Volume",
    "Reserves",
]

tabs = st.tabs(tabs_list)

with tabs[0]:  # Porosidade
    render_porosity()

with tabs[1]:  # Permeability
    render_permeability()

with tabs[2]:  # Resistividade
    render_resistivity()

with tabs[3]:  # Water Saturation
    render_water_saturation()

with tabs[4]:  # Shale Volume
    render_shale_volume()

with tabs[5]:  # Oil Reserves
    render_oil_reserves()
