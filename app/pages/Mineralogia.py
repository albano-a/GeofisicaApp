import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mineralogia",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)

st.title("Mineralogia")
st.write(
    """
Bem-vindo à página de Mineralogia! Aqui você encontrará informações e ferramentas relacionadas ao estudo dos minerais, suas propriedades, classificações e aplicações.
Explore os recursos disponíveis e aprofunde seus conhecimentos sobre o fascinante mundo da mineralogia.
"""
)

st.header("Propriedades dos Minerais")
st.write(
    """
Os minerais possuem diversas propriedades que os tornam únicos. Algumas das principais propriedades incluem:
- **Dureza**: Medida pela escala de Mohs, que classifica os minerais de 1 (talco) a 10 (diamante).
- **Cor**: A aparência do mineral em luz natural.
- **Brilho**: A maneira como a superfície do mineral reflete a luz (metálico, vítreo, etc.).
- **Clivagem**: A tendência de um mineral se partir ao longo de superfícies planas.
- **Densidade**: Relação entre a massa e o volume do mineral.
"""
)

st.header("Tabela de Minerais e Propriedades")
st.write(
    "Abaixo está uma tabela com exemplos de minerais e algumas de suas propriedades:"
)

data = {
    "Classificação": [
        "Silicatos",
        "Silicatos",
        "Silicatos",
        "Silicatos",
        "Silicatos",
        "Silicatos",
        "Silicatos",
        "Óxidos",
        "Sulfetos",
        "Sulfatos",
        "Carbonatos",
        "Haletos",
        "Hidróxidos",
        "Fosfato",
    ],
    "Classe": [
        "Nesossilicatos",
        "Sorossilicatos",
        "Ciclossilicatos",
        "Isossilicatos (Cadeia simples)",
        "Isossilicatos (Cadeia dupla)",
        "Filossilicatos",
        "Tectossilicatos",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ],
    "Radical": [
        "(SiO4)4-",
        "(Si2O7)6-",
        "(Si6O18)12-",
        "(Si2O6)4-",
        "(Si8O22)6-",
        "(Si4O10)4-",
        "(SiO2)0",
        "O2-",
        "S-",
        "SO4-",
        "CO3-",
        "F-, Cl-",
        "(OH)-",
        "PO4-",
    ],
    "Exemplos": [
        "Granada, Olivina, Cianita, Topázio",
        "Epidoto",
        "Turmalina, Berilio",
        "Piroxênio, Espodumênio",
        "Anfibólio",
        "Mica, Caulinita, Esmecita, Talco, Clorita",
        "K-feldspato, Plagioclásio, Quartzo",
        "Hematita, Ileminita, Cassiderita, psilomelano, magnetita e coridon",
        "Esfalerita, Galena, pirita, molibdenita e calcopirita",
        "Barita e Gipsita",
        "Calcita e dolomita",
        "Halita, Fluorita",
        "Bauxita",
        "Apatita",
    ],
}

# Filtro por classificação
classificacao = st.selectbox("Selecione uma Classificação", options=list(set(data["Classificação"])))

# Filtrar os dados
filtered_data = {
    key: [value for i, value in enumerate(values) if data["Classificação"][i] == classificacao]
    for key, values in data.items()
}

# Exibir os resultados filtrados
for i in range(len(filtered_data["Classificação"])):
    st.write(f"### {filtered_data['Classificação'][i]} - {filtered_data['Classe'][i] or 'Não especificado'}")
    st.write(f"**Radical:** {filtered_data['Radical'][i]}")
    st.write(f"**Exemplos:** {filtered_data['Exemplos'][i]}")

st.header("Aplicações dos Minerais")
st.write(
    """
Os minerais têm uma ampla gama de aplicações em diversas indústrias, como:
- **Construção**: Uso de minerais como calcário e granito.
- **Tecnologia**: Minerais como quartzo são usados em componentes eletrônicos.
- **Joalheria**: Gemas preciosas como diamantes, rubis e esmeraldas.
- **Indústria química**: Minerais como halita (sal-gema) são usados na produção de produtos químicos.
"""
)
