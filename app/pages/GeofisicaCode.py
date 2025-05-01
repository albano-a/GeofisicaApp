import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy
import components.sidebar as sidebar
from components.geofisicacode.basic_tab import render_base
from components.geofisicacode.math_tab import render_math
from components.geofisicacode.random_tab import render_random
from components.geofisicacode.numpy_tab import render_numpy
from components.geofisicacode.matplotlib_tab import render_matplotlib
from components.geofisicacode.pandas_tab import render_pandas

st.set_page_config(
    page_title="GeofisicaCode",
    page_icon="assets/geofisicacode_favicons.svg",
    layout="wide",
)

sidebar.show()

st.image("assets/GeofisicaCode.svg", width=600, output_format="PNG")

list_of_tabs_geofisicacode = [
    "Base",
    "Math",
    "Random",
    "Numpy",
    "Matplotlib",
    "Pandas",
]
tabs_geofisicacode = st.tabs(list_of_tabs_geofisicacode)

with tabs_geofisicacode[0]:
    render_base()

with tabs_geofisicacode[1]:
    render_math()

with tabs_geofisicacode[2]:
    render_random()

with tabs_geofisicacode[3]:
    render_numpy()

with tabs_geofisicacode[4]:
    render_matplotlib()

with tabs_geofisicacode[5]:
    render_pandas()

