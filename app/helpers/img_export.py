import streamlit as st
import io


def export_as_svg(fig, fname="placeholder"):
    """Exports matplotlib figures as svg"""
    buf = io.StringIO()
    fig.savefig(buf, format="svg")
    svg_data = buf.getvalue()
    st.download_button(
        label="Download SVG",
        data=svg_data,
        file_name=fname + ".svg",
        mime="image/svg+xml",
    )
    buf.close()
