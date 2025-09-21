import streamlit as st
from components.header import render_header
import components.sidebar as sidebar

# Configure the page
render_header(
    page_title="GeofisicaApp",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

# Get navigation pages from sidebar component
pages = sidebar.get_pages()

# Set up navigation
nav = st.navigation(pages, position="top")

# Run the selected page
nav.run()