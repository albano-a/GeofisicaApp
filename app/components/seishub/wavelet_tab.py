import streamlit as st


def render_wavelet():
    st.write("Wavelet")
    
    _wavelets = ["Ricker", "Butterworth", "Ormsby"]
    
    wavelet = st.tabs(_wavelets)
    
    with wavelet[0]:
        st.write(
            """
            Something something ricker here
            """
        )
