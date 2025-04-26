import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="GeofisicaCode",
    page_icon="assets/geofisicacode_favicons.svg",
    layout="centered",
)

render_sidebar()

st.image("assets/GeofisicaCode.svg", use_container_width=True)

st.title("Welcome to GeofisicaCode")
st.write(
    """
    GeofisicaCode is your go-to platform for geophysical data analysis and visualization.
    Explore the tools and resources we provide to enhance your geophysical workflows.
    """
)

st.header("Features")
st.markdown(
    """
    - **Data Visualization**: Create stunning visualizations of your geophysical data.
    - **Analysis Tools**: Utilize advanced algorithms for data processing.
    - **Custom Workflows**: Tailor the platform to your specific needs.
    """
)

st.header("Get Started")
st.write(
    """
    Use the sidebar to navigate through the application and access various tools and features.
    """
)
