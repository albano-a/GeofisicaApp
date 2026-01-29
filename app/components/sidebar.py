import streamlit as st


def get_pages():
    pages = {
        "Homepage": [st.Page("pages/Homepage.py", title="Homepage", icon=":material/home:")],
        "Geophysics": [
            st.Page(
                "pages/1_GeofisicaCode.py",
                title="GeofisicaCode",
                icon=":material/code:",
            ),
            st.Page("pages/8_SeisHub.py", title="SeisHub", icon=":material/waves:"),
        ],
        "Geology & Minerals": [
            st.Page("pages/2_GeologiHub.py", title="GeologiHub", icon=":material/landscape:"),
            st.Page("pages/3_MineralHub.py", title="MineralHub", icon=":material/diamond:"),
            st.Page(
                "pages/4_PetrofisicaHub.py",
                title="PetrofisicaHub",
                icon=":material/layers:",
            ),
        ],
        "Tools & Analysis": [
            st.Page("pages/5_CalcHub.py", title="CalcHub", icon=":material/calculate:"),
            st.Page("pages/6_FisicaHub.py", title="FisicaHub", icon=":material/science:"),
            st.Page("pages/7_ToolsHub.py", title="ToolsHub", icon=":material/build:"),
        ],
    }

    return pages
