import streamlit as st
import pandas as pd
import os

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

st.subheader("Índice")
st.markdown(
    """
    1. [Propriedades Físicas dos Minerais](#8f4ac04a)
    2. [Tabela de Classificação dos Minerais](#b37688fb)
    3. [Sistemas Cristalinos](#sistemas-cristalinos)
    4. [Dureza](#dureza)
    5. [Identificador de Minerais](#identificador-de-minerais)
    """,
    unsafe_allow_html=True,
)
st.markdown("---")
st.header("Propriedades Fisicas dos Minerais")

with st.expander("**Traço**"):
    st.write(
        """
    É a cor ou risco deixado pelo mineral quando riscado contra uma superfície. 
     
    Ex.: Branco, vermelho, translúcido.
    """,
        unsafe_allow_html=True,
    )
with st.expander("**Dureza**"):
    st.write(
        """
        A resistência de um mineral ao desgaste quando submetido a fricção ou raspagem.
        
        Ex.: de 1 (talco) a 10 (diamante).
        """
    )

with st.expander("**Densidade**"):
    st.write(
        """
    É a relação entre a massa de um material e o volume que ele ocupa. É expressa pela fórmula:
    """
    )
    st.latex(r"\text{Densidade} = \frac{Massa}{Volume} \equiv " r" \rho = \frac{m}{V}")

with st.expander("**Difaneidade**"):
    st.write(
        """
    É a forma como o mineral reage a luz.
    
    Ex.: Transparente, Translúcido ou Opaco.
    """
    )

with st.expander("**Clivagem**"):
    st.write(
        """
    É a forma como o mineral se divide.

    Ex.: Perfeita, Imperfeita, Ausente.
    """
    )
st.markdown("---")
st.header("Tabela de Classificação dos Minerais")
st.write(
    "Abaixo está uma tabela com exemplos de minerais e algumas de suas propriedades:"
)

html = """
<table border="1" style="border-collapse: collapse; width: 100%; text-align: center;">
    <thead style="background:#bc1077">
        <tr>
            <th>Classificação</th>
            <th colspan="2">Classe</th>
            <th>Radical</th>
            <th>Exemplos</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="7">Silicatos</td>
            <td colspan="2">Nesossilicatos</td><td>(SiO4)4-</td><td>Granada, Olivina, Cianita, Topázio</td>
        </tr>
        <tr>
            <td colspan="2">Sorossilicatos</td><td>(Si2O7)6-</td><td>Epidoto</td>
        </tr>
        <tr>
            <td colspan="2">Ciclossilicatos</td><td>(Si6O18)12-</td><td>Turmalina, Berilio</td>
        </tr>
        <tr>
            <td rowspan="2">Isossilicatos</td><td>Cadeia simples</td><td>(Si2O6)4-</td><td>Piroxênio, Espodumênio</td>
        </tr>
        <tr>
            <td>Cadeia dupla</td><td>(Si8O22)6-</td><td>Anfibólio</td>
        </tr>
        <tr>
            <td colspan="2">Filossilicatos</td><td>(Si4O10)4-</td><td>Mica, Caulinita, Esmecita, Talco, Clorita</td>
        </tr>
        <tr>
            <td colspan="2">Tectossilicatos</td><td>(SiO2)0</td><td>K-feldspato, Plagioclásio, Quartzo</td>
        </tr>
        <tr>
            <td colspan="3">Óxidos</td><td>O2-</td><td>Hematita, Ileminita, Cassiderita, Psilomelano, Magnetita, Coridon</td>
        </tr>
        <tr>
            <td colspan="3">Sulfetos</td><td>S-</td><td>Esfalerita, Galena, Pirita, Molibdenita, Calcopirita</td>
        </tr>
        <tr>
            <td colspan="3">Sulfatos</td><td>SO4-</td><td>Barita, Gipsita</td>
        </tr>
        <tr>
            <td colspan="3">Carbonatos</td><td>CO3-</td><td>Calcita, Dolomita</td>
        </tr>
        <tr>
            <td colspan="3">Haletos</td><td>F-, Cl-</td><td>Halita, Fluorita</td>
        </tr>
        <tr>
            <td colspan="3">Hidróxidos</td><td>(OH)-</td><td>Bauxita</td>
        </tr>
        <tr>
            <td colspan="3">Fosfato</td><td>PO4-</td><td>Apatita</td>
        </tr>
    </tbody>
</table>
"""

st.markdown(html, unsafe_allow_html=True)
st.markdown("---")
st.header("Sistemas Cristalinos")

with st.expander("**Cúbico**"):
    st.write(
        "Três eixos iguais e perpendiculares, formando cubos perfeitos. Também chamado de isométrico. Ex.: Pirita, Diamante, Galena."
    )
    cols = st.columns(3)
    with cols[0]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2018/02/Pirita-6-400x400.jpg",
            width=200,
            caption="**Pirita**",
        )
    with cols[1]:
        st.image("assets/cristalinos/cubico.png", width=200)
    with cols[2]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2018/02/Galena-2-400x400.jpg",
            width=200,
            caption="**Galena**",
        )

with st.expander("**Monoclínico**"):
    st.write("Três eixos desiguais, dois perpendiculares e um inclinado. Ex.: Gipsita.")
    cols = st.columns(3, gap="medium")
    with cols[0]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2017/09/Gipsita_2-400x400.jpg",
            width=200,
            caption="**Gipsita**",
        )
    with cols[1]:
        st.image("assets/cristalinos/monoclinico.png", width=200)
    with cols[2]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2017/09/Gipsita_6-400x400.jpg",
            width=200,
            caption="**Gipsita**",
        )

with st.expander("**Triclínico**"):
    st.write(
        "Três eixos desiguais e inclinados entre si, sem ângulos retos. Ex.: Turquesa."
    )
    cols = st.columns(3)
    with cols[0]:
        st.image(
            "https://kaviah.com/wp-content/uploads/2021/02/turquesa-capa.jpg",
            width=200,
            caption="**Turquesa**",
        )
    with cols[1]:
        st.image("assets/cristalinos/triclinico.png", width=200)
    with cols[2]:
        st.image(
            "https://i0.wp.com/geologyscience.com/wp-content/uploads/2019/07/Turquoise-pyrite-quartz.jpeg?resize=640%2C425&ssl=1",
            width=200,
            caption="**Turquesa**",
        )

with st.expander("**Ortorrômbico**"):
    st.write("Três eixos desiguais, todos perpendiculares entre si. Ex.: Topázio.")
    cols = st.columns(3)
    with cols[0]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2019/01/Topazio-16-400x400.jpg",
            width=200,
            caption="**Topázio**",
        )
    with cols[1]:
        st.image("assets/cristalinos/ortorrombico.png", width=200)
    with cols[2]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2018/02/Top%C3%A1zio-2-400x400.jpg",
            width=200,
            caption="**Topázio**",
        )

with st.expander("**Romboédrico**"):
    st.write(
        "Três eixos iguais com ângulos iguais mas diferentes de 90°. Ex.: Calcita."
    )
    cols = st.columns(3)
    with cols[0]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2019/02/Calcita-17-400x400.jpg",
            width=200,
            caption="**Calcita**",
        )
    with cols[1]:
        st.image("assets/cristalinos/romboedrico.png", width=200)
    with cols[2]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2019/02/Calcita-16-400x400.jpg",
            width=200,
            caption="**Calcita**",
        )

with st.expander("**Tetragonal**"):
    st.write("Dois eixos iguais, um diferente, todos perpendiculares. Ex.: Zircão.")
    cols = st.columns(3)
    with cols[0]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2020/03/zircao-1-400x400.jpg",
            width=200,
            caption="**Zircão**",
        )
    with cols[1]:
        st.image("assets/cristalinos/tetragonal.png", width=200)
    with cols[2]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2020/03/zircao-2-400x400.jpg",
            width=200,
            caption="**Zircão**",
        )

with st.expander("**Hexagonal**"):
    st.write(
        "Dois eixos iguais em 120°, e um eixo diferente perpendicular a eles. Ex.: Berilo."
    )
    cols = st.columns(3)
    with cols[0]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2019/02/Berilo-26-400x400.jpg",
            width=200,
            caption="**Berilo**",
        )
    with cols[1]:
        st.image("assets/cristalinos/hexagonal.png", width=200)
    with cols[2]:
        st.image(
            "https://museuhe.com.br/site/wp-content/uploads/2019/02/Berilo-27-400x400.jpg",
            width=200,
            caption="**Berilo**",
        )
st.markdown("---")
st.header("Dureza")

html_dureza = """
<table border="1" style="border-collapse: collapse; width: 100%; text-align: center;">
    <thead style="background:#bc1077">
        <tr>
            <th>Valor de Dureza</th>
            <th>Mineral exemplo</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Talco</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Gipsita</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Calcita</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Fluorita</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Apatita</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Feldspato</td>
        </tr>
        <tr>
            <td>7</td>
            <td>Quartzo</td>
        </tr>
        <tr>
            <td>8</td>
            <td>Topázio</td>
        </tr>
        <tr>
            <td>9</td>
            <td>Coríndon</td>
        </tr>
        <tr>
            <td>10</td>
            <td>Diamante</td>
        </tr>
    </tbody>
</table>
"""

st.markdown(html_dureza, unsafe_allow_html=True)
st.markdown("---")

st.header("Identificador de Minerais")

df = pd.read_csv("assets/data/mineral_identifier.csv")

st.subheader("Escolha as propriedades observadas:")

cores_unicas = []
for c in df["cor"]:
    cores_unicas.extend(c.lower().split("-"))
cores_unicas = sorted(list(set(cores_unicas)))

cor_in = st.selectbox("Cor", options=cores_unicas)
brilho_opts = ["Não sei"] + sorted(df["brilho"].dropna().unique())
brilho_in = st.selectbox("Brilho", options=brilho_opts)

fratura_opts = ["Não sei"] + sorted(df["fratura"].dropna().unique())
fratura_in = st.selectbox("Fratura", options=fratura_opts)

habito_opts = ["Não sei"] + sorted(df["hábito"].dropna().unique())
habito_in = st.selectbox("Hábito", options=habito_opts)

diaf_unicas = []
for d in df["diafaneidade"]:
    diaf_unicas.extend(d.lower().split("-"))
diaf_unicas = sorted(list(set(diaf_unicas)))

diafaneidade_in = st.selectbox(
    "Diafaneidade",
    options=diaf_unicas,
    help="Diafaneidade é a propriedade do mineral de reagir a luz.",
)

dureza_in = st.slider("Dureza (escala Mohs)", 1.0, 10.0, step=0.5)

usar_densidade = st.checkbox("Considerar densidade?")
dens_in = st.slider("Densidade (g/cm³)", 1.0, 25.0, step=0.1)

usar_magnetismo = st.checkbox("Considerar magnetismo?")
magnet_in = st.selectbox("O mineral é magnético?", options=["Não sei", "Sim", "Não"])

filtrar_60 = st.checkbox("Mostrar apenas resultados com match > 60%")

pesos = {
    "cor": 1,
    "brilho": 1.5,
    "fratura": 1,
    "hábito": 1,
    "dureza": 2,
    "densidade": 2,
    "magnetismo": 3,
    "diafaneidade": 1.5,
}

if st.button("Identificar"):
    resultados = []

    for _, row in df.iterrows():
        score = 0
        total = 0

        # Cor (obrigatória)
        total += 1
        if cor_in.lower() in str(row["cor"]).lower():
            score += pesos["cor"]

        # Brilho
        if brilho_in != "Não sei":
            total += pesos["brilho"]
            if brilho_in == row["brilho"]:
                score += pesos["brilho"]

        # Fratura
        if fratura_in != "Não sei":
            total += pesos["fratura"]
            if fratura_in == row["fratura"]:
                score += pesos["fratura"]

        # Hábito
        if habito_in != "Não sei":
            total += pesos["hábito"]
            if habito_in == row["hábito"]:
                score += pesos["hábito"]

        if diafaneidade_in != "Não sei":
            total += pesos["diafaneidade"]
            if diafaneidade_in == row["diafaneidade"]:
                score += pesos["diafaneidade"]

        # Dureza
        try:
            min_dur = float(str(row["dureza"]).split("-")[0])
            max_dur = float(str(row["dureza"]).split("-")[-1])
            total += pesos["dureza"]
            if min_dur <= dureza_in <= max_dur:
                score += pesos["dureza"]
        except:
            pass

        # Densidade
        if usar_densidade:
            try:
                min_dens = float(str(row["densidade"]).split("-")[0])
                max_dens = float(str(row["densidade"]).split("-")[-1])
                total += pesos["densidade"]
                if min_dens <= dens_in <= max_dens:
                    score += pesos["densidade"]
            except:
                pass

        # Magnetismo
        if usar_magnetismo and magnet_in != "Não sei":
            total += pesos["magnetismo"]
            if str(row["magnetismo"]).lower() == magnet_in.lower():
                score += pesos["magnetismo"]

        if cor_in.lower() not in str(row["cor"]).lower():
            score -= pesos["cor"] * 0.1  # Penaliza se cor não bater

        match_pct = (score / total) * 100 if total > 0 else 0

        resultados.append(
            {
                "Nome": row["nome"],
                "Match (%)": round(match_pct, 1),
                "Cor": row["cor"],
                "Brilho": row["brilho"],
                "Dureza": row["dureza"],
                "Fratura": row["fratura"],
                "Hábito": row["hábito"],
                "Densidade": row.get("densidade", "N/A"),
                "Magnético": row.get("magnetismo", "N/A"),
                "Diafaneidade": row["diafaneidade"],
            }
        )

    df_result = pd.DataFrame(resultados)
    df_result = df_result[df_result["Match (%)"] > 0]  # <-- Remove match 0
    df_result = df_result.sort_values(by="Match (%)", ascending=False)

    def colorize_match(val):
        if val > 80:
            return "background-color: #1c3d2b; color: #dffde9"
        elif val >= 60:
            return "background-color: #fff2cc; color: #7f6000"
        else:
            return "background-color: #f4cccc; color: #990000"

    #

    if not df_result.empty:
        if filtrar_60:
            df_result = df_result[df_result["Match (%)"] >= 60]

        historico = (
            pd.read_csv("historico.csv")
            if os.path.exists("historico.csv")
            else pd.DataFrame()
        )
        historico = pd.concat([historico, df_result], ignore_index=True)
        historico.to_csv("historico.csv", index=False)

        df_result_styled = df_result.style.map(
            colorize_match, subset=["Match (%)"]
        )

        st.success("Minerais compatíveis encontrados:")
        st.dataframe(df_result_styled)

        if st.button("Baixar histórico"):
            # Salva o histórico
            st.download_button(
                label="Download do Histórico",
                data=historico.to_csv(index=False),
                file_name="historico.csv",
                mime="text/csv",
            )

    else:
        st.warning("Nenhum mineral encontrado com essas características.")
