import streamlit as st
import components.sidebar as sidebar
from helpers.parser_calc import MathTransformer, math_parser
from components.header import render_header

import math

render_header(
    page_title="CalcHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.image("assets/CalcHub.png", width="stretch", output_format="PNG")

st.info(
    "Estamos trabalhando para lançar esta página em breve.",
    icon=":material/construction:",
)


math_transformer = MathTransformer()

# Streamlit interface for the calculator
st.subheader("Calculadora Matemática")

equation = st.text_input(
    "Digite uma equação matemática:", placeholder="2 + 3 * sin(pi/2)"
)

if equation:
    try:
        parse_tree = math_parser.parse(equation)
        result = math_transformer.transform(parse_tree)
        st.success(f"Resultado: {result}")
    except Exception as e:
        st.error(f"Erro ao processar a equação: {str(e)}")

# Example equations
st.subheader("Exemplos:")
examples = [
    "2 + 3 * 4",
    "sin(pi/2) + cos(0)",
    "sqrt(16) + log(e)",
    "2^3 + 5",
    "(2 + 3) * (4 - 1)",
]

for example in examples:
    if st.button(f"Testar: {example}"):
        try:
            parse_tree = math_parser.parse(example)
            result = math_transformer.transform(parse_tree)
            st.write(f"**{example}** = {result}")
        except Exception as e:
            st.error(f"Erro: {str(e)}")
