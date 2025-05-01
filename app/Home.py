import streamlit as st
import components.sidebar as sidebar
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="GeofisicaApp",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
    menu_items={
        "About": """
        Esse aplicativo faz parte do ecossistema
        do GeofisicaHub.
        
        #### Desenvolvido por André Albano
        """
    },
)

sidebar.show()

st.image("assets/GeofisicaApp_beta.png", use_container_width=True)
st.info(
    "Estamos trabalhando para lançar este site em breve.",
    icon=":material/construction:",
)
st.write(
    """
    Explore os conteúdos disponíveis abaixo:
    """
)


columns = st.columns(3, gap="small", border=True)

with columns[0]:
    st.write(
        """
        <h4 style="color:#6a6c70">GeofísicaCode</h4>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui",
        url="Geologia",
        type="primary",
        icon=":material/public:",
        use_container_width=True,
        disabled=True,
    )


with columns[1]:
    st.write(
        """
        #### Geologia
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui",
        url="Geologia",
        type="primary",
        icon=":material/layers:",
        use_container_width=True,
    )

with columns[2]:
    st.write(
        """
        #### MineralHub
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui",
        url="MineralHub",
        type="primary",
        icon=":material/diamond:",
        use_container_width=True,
    )
    # ste.editor().Monaco()

columns = st.columns(3, gap="small", border=True)

with columns[0]:
    st.write(
        """
        #### PetrofisicaHub
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui",
        url="PetrofisicaHub",
        type="primary",
        icon=":material/stacked_line_chart:",
        use_container_width=True,
    )
    # ste.editor().Monaco()

with columns[1]:
    st.write(
        """
        <h4 style="color:#6a6c70">Cálculo</h4>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui",
        url="",
        type="primary",
        icon=":material/functions:",
        use_container_width=True,
        disabled=True,
    )

with columns[2]:
    st.write(
        """
        <h4 style="color:#6a6c70">Física</h4>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui",
        url="",
        type="primary",
        icon=":material/orbit:",
        use_container_width=True,
        disabled=True,
    )
