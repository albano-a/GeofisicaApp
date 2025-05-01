import streamlit as st
from components.crystalography import generate_crystal
import components.mineral_id as mineral_id
import components.sidebar as sidebar

st.set_page_config(
    page_title="MineralHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)
sidebar.show()

st.image("assets/MineralHub.png", use_container_width=True, output_format="PNG")
st.write(
    """
Bem-vindo à página de Mineralogia! Aqui você encontrará apps e ferramentas relacionadas ao estudo dos minerais, suas propriedades, classificações e aplicações.
Explore os recursos disponíveis e aprofunde seus conhecimentos sobre o mundo da mineralogia.
"""
)


tabs_min = [
    "Propriedades Físicas",
    "Classificação",
    "Sistemas Cristalinos",
    "Dureza",
    "Identificador de Minerais",
]
tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs_min)

with tab1:
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
        st.latex(
            r"\text{Densidade} = \frac{Massa}{Volume} \equiv " r" \rho = \frac{m}{V}"
        )

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

with tab2:
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

with tab3:

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
        st.write(
            "Três eixos desiguais, dois perpendiculares e um inclinado. Ex.: Gipsita."
        )
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

    st.header("Visualizador de Sistema cristalino")

    type = st.pills(
        label="Escolha um sistema cristalino:",
        default="Cúbico",
        options=[
            "Cúbico",
            "Tetragonal",
            "Ortorrômbico",
            "Hexagonal",
            "Triclínico",
            "Monoclínico",
            "Romboédrico",
        ],
    )

    fig = generate_crystal(type)
    st.plotly_chart(fig)

with tab4:
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

with tab5:
    st.header("Identificador de Minerais")

    st.write("Escolha as propriedades observadas:")
    st.divider()

    mineral_id.run()
