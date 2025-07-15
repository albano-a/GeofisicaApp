import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy
from components.header import render_header
from components.geofisicacode.basic_tab import render_base
from components.geofisicacode.math_tab import render_math
from components.geofisicacode.random_tab import render_random
from components.geofisicacode.numpy_tab import render_numpy
from components.geofisicacode.matplotlib_tab import render_matplotlib
from components.geofisicacode.pandas_tab import render_pandas

render_header(
    page_title="GeofisicaCode",
    page_icon="assets/geofisicacode_favicons.svg",
    layout="wide",
    menu_items={
        "About": """
        This application is part of the GeofisicaHub ecosystem.
        
        #### Developed by André Albano
        """
    },
)

st.image("assets/GeofisicaCode.svg", width=600, output_format="PNG")
st.warning(
    "This page is under construction. More code examples will be added soon!",
    icon="🚧",
)
st.write(
    "🐍 Python is great for data science! Here's a cheat sheet with useful code examples."
)

list_of_tabs_geofisicacode = [
    "Base",
    "Math",
    "Random",
    "Numpy",
    "Matplotlib",
    "Pandas",
    "Segyio",
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

with tabs_geofisicacode[6]:
    pass
