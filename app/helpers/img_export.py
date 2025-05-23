import streamlit as st
import io


def export_as_svg(fig, fname="placeholder", fformat="svg", dpi=500):
    """Exports matplotlib figures in any format with adjustable DPI"""
    buf = io.BytesIO()
    fig.savefig(buf, format=fformat, dpi=dpi)
    buf.seek(0)
    data = buf.read()
    # determine MIME type
    fmt = fformat.lower()
    if fmt == "svg":
        mime = "image/svg+xml"
    elif fmt == "pdf":
        mime = "application/pdf"
    else:
        mime = f"image/{fmt}"
    st.download_button(
        label=f"Download {fformat}",
        data=data,
        file_name=f"{fname}.{fformat}",
        mime=mime,
        use_container_width=True,
    )
    buf.close()
