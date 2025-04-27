import streamlit as st
from streamlit_elements import elements, editor, dashboard
import components.sidebar as sidebar
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

sidebar.show()

st.image("assets/GeofisicaApp.svg", use_container_width=True)

st.subheader("Conteúdos e Aplicativos da Geofísica")

st.write(
    """
         Explore os conteúdos abaixo:
         """
)

columns = st.columns(3, gap="small", border=True)

with columns[0]:
    st.write(
        """
        #### Mineralogia
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui", url="Mineralogia", type="primary", use_container_width=True
    )
    # ste.editor().Monaco()

with columns[1]:
    st.write(
        """
        #### Geologia
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui", url="Geologia", type="primary", use_container_width=True
    )

with columns[2]:
    st.write(
        """
        #### GeofisicaCode
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui", url="Geologia", type="primary", use_container_width=True
    )

columns = st.columns(3, gap="small", border=True)

with columns[0]:
    st.write(
        """
        ### PetroCalc
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui", url="Petrofisica", type="primary", use_container_width=True
    )
    # ste.editor().Monaco()

with columns[1]:
    st.write(
        """
        ### 
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui", url="Geologia", type="primary", use_container_width=True
    )

with columns[2]:
    st.write(
        """
        ### 
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Clique aqui", url="Geologia", type="primary", use_container_width=True
    )
