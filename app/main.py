import streamlit as st
from streamlit_elements import elements, editor, dashboard
from components.sidebar import render_sidebar
import pages.Mineralogia as mineralogia


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

render_sidebar()

st.image("assets/GeofisicaApp.svg", use_container_width=True)

st.subheader("Conteúdos e Aplicativos da Geofísica")

st.write(
    """
         Explore os conteúdos abaixo:
         """
)

columns = st.columns([1, 1, 1], gap="large", border=True)

with columns[0]:
    st.write(
        """
        
        """
    )
    # ste.editor().Monaco()

with columns[1]:
    st.write(
        """
             
             """
    )

with columns[2]:
    st.write(
        """
        
        """
    )
