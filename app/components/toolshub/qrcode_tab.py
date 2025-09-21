import streamlit as st
import qrcode.constants
import streamlit as st
from components.header import render_header
import random
import pandas as pd
import qrcode
import io


def render_qrcode():
    st.subheader("Generate QR Code to any link you have.")
    link = st.text_input("Link")

    if st.button("Generate", width="stretch"):
        if link.strip():
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#000000", back_color="#ffffff")

            # Save QR Code to buffer
            buf = io.BytesIO()
            img.save(buf, format="PNG")

            # Display and download QR Code
            cols = st.columns(3)
            with cols[1]:
                st.image(buf.getvalue(), width=200)
            st.download_button(
                label="Download QR Code",
                data=buf.getvalue(),
                file_name="qrcode.png",
                mime="image/png",
                width="stretch",
            )
        else:
            st.warning("Please enter a valid link.")
