import streamlit as st



def render_header(
    page_title,
    page_icon,
    layout,
    menu_items=None,
):
    st.set_page_config(
        page_title=page_title, page_icon=page_icon, layout=layout, menu_items=menu_items
    )


    # hide_streamlit_style = """
    #         <style>
    #         #MainMenu {visibility: hidden;}
    #         footer {visibility: hidden;}
    #         </style>
    #         """
    # st.markdown(hide_streamlit_style, unsafe_allow_html=True)
