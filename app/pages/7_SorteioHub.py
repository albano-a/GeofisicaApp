import streamlit as st
from components.header import render_header
import random
import pandas as pd
import io

render_header(
    page_title="SorteioHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.title("SorteiosHub")
st.subheader("Sorteie nomes, números ou qualquer item.")

tipo = st.selectbox("Escolha o tipo de sorteio:", ["Nomes/Itens", "Números"])

unique = st.checkbox("Evitar repetições?", value=True)
qtd = st.number_input("Quantidade de sorteios:", min_value=1, max_value=1000, value=1)

if "historico" not in st.session_state:
    st.session_state.historico = set()


def reset_history():
    st.session_state.historico.clear()


if tipo == "Nomes/Itens":
    op = st.radio(
        "Como deseja fornecer os itens?",
        ["Escrever manualmente", "Upload de arquivo (.txt, .csv)"],
    )

    lista = []

    if op == "Escrever manualmente":
        texto = st.text_area("Digite os itens (um por linha):")
        if texto:
            lista = [i.strip() for i in texto.splitlines() if i.strip()]
    else:
        uploaded_file = st.file_uploader("Envie o arquivo:", type=["txt", "csv"])
        if uploaded_file:
            ext = uploaded_file.name.split(".")[-1]
            if ext == "txt":
                data = uploaded_file.read().decode("utf-8")
                lista = [i.strip() for i in data.splitlines() if i.strip()]

            elif ext == "csv":
                df = pd.read_csv(uploaded_file)
                col = st.selectbox("Escolha a coluna:", df.columns)
                lista = df[col].dropna().astype(str).tolist()

    if lista:
        lista_unica = list(set(lista)) if unique else lista
        restante = (
            list(set(lista_unica) - st.session_state.historico)
            if unique
            else lista_unica
        )

        if not restante:
            st.warning("Todos os itens já foram sorteados.")
        elif st.button("Sortear"):
            sorteados = random.sample(restante, min(qtd, len(restante)))
            for s in sorteados:
                st.write(f"🎉 {s}")
                st.session_state.historico.add(s)

            st.success("Sorteio realizado!")

elif tipo == "Números":
    min_val = st.number_input("Valor mínimo:", value=1)
    max_val = st.number_input("Valor máximo:", value=100)

    if min_val >= max_val:
        st.error("O valor máximo deve ser maior que o mínimo.")
    else:
        universo = list(range(int(min_val), int(max_val) + 1))
        restante = (
            list(set(universo) - st.session_state.historico) if unique else universo
        )

        if not restante:
            st.warning("Todos os números já foram sorteados.")
        elif st.button("Sortear"):
            sorteados = random.sample(restante, min(qtd, len(restante)))
            for s in sorteados:
                st.write(f"🎉 {s}")
                st.session_state.historico.add(s)
            st.success("Sorteio realizado!")

# Resetar histórico
if unique:
    st.divider()
    if st.button("🔄 Resetar histórico de sorteios"):
        reset_history()
        st.info("Histórico limpo com sucesso.")
