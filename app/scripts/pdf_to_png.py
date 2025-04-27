import streamlit as st
from pdf2image import convert_from_path
import io


# Função para converter PDF em imagem e exibir no Streamlit
def show_pdf_page_as_image(pdf_path, page_number=0, dpi=500):
    # Converter o PDF para uma lista de imagens (uma imagem por página)
    images = convert_from_path(
        pdf_path, first_page=page_number + 1, last_page=page_number + 1, dpi=dpi
    )

    # Obter a imagem da página desejada
    img = images[0]

    # Salvar a imagem em um buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Exibir a imagem no Streamlit
    st.image(buf, caption="Tabela", use_container_width=True)
