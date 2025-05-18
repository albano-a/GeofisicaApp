import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import openpyxl

from components.header import render_header

render_header(
    page_title="GeologiHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.image("assets/GeologiHub.png", use_container_width=True, output_format="PNG")

st.header("Tabela Cronoestratigráfica")

# Caminho do arquivo PDF
pdf_path = "assets/data/chrono_chart.png"

# Exibir a página 1 do PDF como imagem
st.image(pdf_path, caption="Tabela Cronoestratigráfica", use_container_width=True)

wb = openpyxl.load_workbook("assets/data/cronoestratigrafica.xlsx")
ws = wb.active

dados = []

for row in ws.iter_rows(
    min_row=2, values_only=True
):  # Começando da segunda linha para pular os títulos
    linha = []
    for cell in row:
        linha.append(cell)
    dados.append(linha)


colunas = ["Pre-eon", "Eon", "Era", "Period", "Epoch", "Age", "Start (Ma)", "End (Ma)"]
dados = dados[1:]
df = pd.DataFrame(dados, columns=colunas)


df["Start (Ma)"] = pd.to_numeric(df["Start (Ma)"], errors="coerce")
df["End (Ma)"] = pd.to_numeric(df["End (Ma)"], errors="coerce")

import random

df["Cor"] = [
    "#" + "".join(random.choices("0123456789ABCDEF", k=6)) for _ in range(len(df))
]

fig = go.Figure()

for idx, row in df.iterrows():
    start_ma = row["Start (Ma)"]
    end_ma = row["End (Ma)"]
    width = start_ma - end_ma if start_ma > end_ma else end_ma - start_ma

    color = row.get("Cor", "rgba(255, 165, 0, 0.7)")

    # Firt we use epoch then age as y axis
    epoch = row["Epoch"] if row["Epoch"] != "-" else "No epoch"
    age = row["Age"] if row["Age"] != "-" else "No Age available"
    period = row["Period"] if row["Period"] != "-" else "Sem Período"

    # Gerar uma chave única combinando a época e o período
    y_label = f"{period} - {epoch}" if epoch != "Sem Epoch" else f"{period} - {age}"

    fig.add_trace(
        go.Bar(
            y=[y_label],
            x=[width],
            base=min(start_ma, end_ma),  # A base deve ser o valor menor
            orientation="h",
            # marker=dict(color=color),
            name=row["Age"],
            hovertemplate=(
                f"<b>{row['Age']}</b><br>"
                f"Idade: {age}<br>"
                f"Época: {epoch}<br>"
                f"Período: {period}<br>"
                f"Éon: {row['Eon']}<br>"
                f"Início: {start_ma} Ma<br>"
                f"Fim: {end_ma} Ma<br>"
            ),
        )
    )

fig.update_layout(
    barmode="stack",
    xaxis=dict(
        autorange="reversed",
        type="log",  # Escala logarítmica
        title="Milhões de anos atrás (Ma)",
        tickmode="array",  # Para um controle mais preciso sobre os ticks
        ticks="outside",  # Ticks fora do gráfico
        tickvals=[1, 10, 100, 1000, 10000, 100000],  # Exemplo de valores de ticks
        ticktext=["1", "10", "100", "1K", "10K", "100K"],  # Texto dos ticks
    ),
    height=600,
    width=900,
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
)

st.plotly_chart(fig)

st.divider()

st.header("Conversor de Idades")

idade = st.number_input("Digite a idade (Ma):", min_value=0.0, format="%.4f")

df = pd.read_excel("assets/data/cronoestratigrafica.xlsx")
df["Start (Ma)"] = pd.to_numeric(df["Start (Ma)"], errors="coerce")
df["End (Ma)"] = pd.to_numeric(df["End (Ma)"], errors="coerce")

# Remover linhas que não têm Start ou End válidos
df = df.dropna(subset=["Start (Ma)", "End (Ma)"])

# Ordenar pra garantir que maiores Start venham primeiro
df = df.sort_values(by="Start (Ma)", ascending=False)

# Encontrar o intervalo certo
linha = df.loc[(df["Start (Ma)"] >= idade) & (df["End (Ma)"] < idade)]

if not linha.empty:
    linha = linha.iloc[0]
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Eon", linha["Eon"])
        st.metric("Período", linha["Period"])
        st.metric("Idade", linha["Age"])
    with col2:
        st.metric("Era", linha["Era"])
        st.metric("Época", linha["Epoch"])
        st.metric("Intervalo (Ma)", f"{linha['Start (Ma)']} - {linha['End (Ma)']}")
else:
    st.warning("Idade fora do intervalo conhecido na tabela.")
