import streamlit as st # type: ignore
from components.header import render_header

GEOFISICACODE = "pages/1_GeofisicaCode.py"
GEOLOGIHUB = "pages/2_GeologiHub.py"
MINERALHUB = "pages/3_MineralHub.py"
PETROFISICAHUB = "pages/4_PetrofisicaHub.py"
CALCHUB = "pages/5_CalcHub.py"
FISICAHUB = "pages/6_FisicaHub.py"
SEISHUB = "pages/8_SeisHub.py"
PAGE_LABEL = "Acessar aplicativo :material/arrow_right_alt:"

render_header(
    page_title="GeofisicaApp",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)


st.image("assets/GeofisicaApp_beta.png", use_container_width=True)
st.info(
    "We are working to launch this site soon.",
    icon="🚧",
)
st.write(
    """
    Explore the applications below:
    """
)

with st.expander("GeofísicaCode", icon=":material/public:"):
    st.write(
        """
        Codes for the main Python libraries and the language itself.
        """
    )
    st.page_link(
        page=GEOFISICACODE,
        label=PAGE_LABEL,
    )

with st.expander("GeologiHub", icon=":material/layers:"):
    st.write(
        """
        Contains the chronostratigraphic table and a geological age converter.
        """
    )
    st.page_link(
        page=GEOLOGIHUB,
        label=PAGE_LABEL,
    )

with st.expander("SeisHub", icon=":material/waves:"):
    st.write(
        """
        Under production.
        """
    )
    st.page_link(
        page=SEISHUB,
        label=PAGE_LABEL,
        disabled=True,
    )

with st.expander("MineralHub", icon=":material/diamond:"):
    st.page_link(
        page=MINERALHUB,
        label=PAGE_LABEL,
    )

with st.expander("PetrofisicaHub", icon=":material/stacked_line_chart:"):
    st.page_link(
        page=PETROFISICAHUB,
        label=PAGE_LABEL,
    )

with st.expander("CalcHub", icon=":material/functions:"):
    st.write(
        """
        <h4 style="color:#6a6c70">CalcHub</h4>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        page=CALCHUB,
        label=PAGE_LABEL,
        disabled=True,
    )


with st.expander("FisicaHub", icon=":material/orbit:"):
    st.page_link(
        page=FISICAHUB,
        label=PAGE_LABEL,
        disabled=True,
    )
