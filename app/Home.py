import streamlit as st
from components.header import render_header

GEOFISICACODE = "pages/1_GeofisicaCode.py"
GEOLOGIHUB = "pages/2_GeologiHub.py"
SEISHUB = "pages/3_SeisHub.py"
MINERALHUB = "pages/4_MineralHub.py"
PETROFISICAHUB = "pages/5_PetrofisicaHub.py"
CALCHUB = "pages/6_CalcHub.py"
FISICAHUB = "pages/7_FisicaHub.py"
PAGE_LABEL = "Acessar aplicativo :material/arrow_right_alt:"

render_header(
    page_title="GeofisicaApp",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)


st.image("assets/GeofisicaApp_beta.png", use_container_width=True)
st.info(
    "Estamos trabalhando para lançar este site em breve.",
    icon=":material/construction:",
)
st.write(
    """
    Explore os aplicativos abaixo:
    """
)


with st.expander("GeofísicaCode", icon=":material/public:"):
    st.write(
        """
        Códigos para as principais bibliotecas do Python e da própria linguagem em si.
        """
    )
    st.page_link(
        page=GEOFISICACODE,
        label=PAGE_LABEL,
    )


with st.expander("GeologiHub", icon=":material/layers:"):
    st.write(
        """
        Contém a tabela cronoestratigráfica e um conversor de idades geológicas
        """
    )
    st.page_link(
        page=GEOLOGIHUB,
        label=PAGE_LABEL,
    )

with st.expander("SeisHub", icon=":material/waves:"):
    st.write(
        """
        Em produção
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
    # ste.editor().Monaco()

with st.expander("PetrofisicaHub", icon=":material/stacked_line_chart:"):
    st.page_link(
        page=PETROFISICAHUB,
        label=PAGE_LABEL,
    )
    # ste.editor().Monaco()

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
