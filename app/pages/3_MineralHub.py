import streamlit as st
import components.mineral_id as mineral_id
import components.sidebar as sidebar

from components.crystalography import generate_crystal
from components.header import render_header

render_header(
    page_title="MineralHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)


st.image("assets/MineralHub.png", use_container_width=True, output_format="PNG")


st.write(
    (
        """
    Welcome to the Mineralogy page! 
    Here you will find apps and tools
    related to the study of minerals, 
    their properties, classifications, 
    and applications. Explore the available 
    resources and deepen your knowledge about 
    the world of mineralogy.
    """
    )
)

tabs_min = [
    ("Physical Properties"),
    ("Classification"),
    ("Crystal Systems"),
    ("Hardness"),
    ("Mineral Identifier"),
]
tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs_min)

with tab1:
    st.header(("Physical Properties of Minerals"))

    with st.expander(("**Streak**")):
        st.write(
            (
                """
                The color or mark left by the mineral when scratched against a surface. 
                
                Ex.: White, red, translucent.
                """
            ),
            unsafe_allow_html=True,
        )
    with st.expander(("**Hardness**")):
        st.write(
            (
                """
            The resistance of a mineral to wear when subjected to friction or scraping.
            
            Ex.: from 1 (talc) to 10 (diamond).
            """
            )
        )

    with st.expander(("**Density**")):
        st.write(
            (
                """
        The relationship between the mass of a material and the volume it occupies. It is expressed by the formula:
        """
            )
        )
        st.latex(r"\text{Density} = \frac{Mass}{Volume} \equiv " r" \rho = \frac{m}{V}")

    with st.expander(("**Diaphaneity**")):
        st.write(
            (
                """
                The way the mineral interacts with light.
                
                Ex.: Transparent, Translucent, or Opaque.
                """
            )
        )

    with st.expander(("**Cleavage**")):
        st.write(
            (
                """
        The way the mineral splits.

        Ex.: Perfect, Imperfect, Absent.
        """
            )
        )

with tab2:
    st.header("Mineral Classification Table")
    st.write("Below is a table with examples of minerals and some of their properties:")

    html = """
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: center;">
        <thead style="background:#bc1077">
            <tr>
                <th>Classification</th>
                <th colspan="2">Class</th>
                <th>Radical</th>
                <th>Examples</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td rowspan="7">Silicates</td>
                <td colspan="2">Nesosilicates</td><td>(SiO4)4-</td><td>Garnet, Olivine, Kyanite, Topaz</td>
            </tr>
            <tr>
                <td colspan="2">Sorosilicates</td><td>(Si2O7)6-</td><td>Epidote</td>
            </tr>
            <tr>
                <td colspan="2">Cyclosilicates</td><td>(Si6O18)12-</td><td>Tourmaline, Beryl</td>
            </tr>
            <tr>
                <td rowspan="2">Inosilicates</td><td>Single Chain</td><td>(Si2O6)4-</td><td>Pyroxene, Spodumene</td>
            </tr>
            <tr>
                <td>Double Chain</td><td>(Si8O22)6-</td><td>Amphibole</td>
            </tr>
            <tr>
                <td colspan="2">Phyllosilicates</td><td>(Si4O10)4-</td><td>Mica, Kaolinite, Smectite, Talc, Chlorite</td>
            </tr>
            <tr>
                <td colspan="2">Tectosilicates</td><td>(SiO2)0</td><td>K-feldspar, Plagioclase, Quartz</td>
            </tr>
            <tr>
                <td colspan="3">Oxides</td><td>O2-</td><td>Hematite, Ilmenite, Cassiterite, Psilomelane, Magnetite, Corundum</td>
            </tr>
            <tr>
                <td colspan="3">Sulfides</td><td>S-</td><td>Sphalerite, Galena, Pyrite, Molybdenite, Chalcopyrite</td>
            </tr>
            <tr>
                <td colspan="3">Sulfates</td><td>SO4-</td><td>Barite, Gypsum</td>
            </tr>
            <tr>
                <td colspan="3">Carbonates</td><td>CO3-</td><td>Calcite, Dolomite</td>
            </tr>
            <tr>
                <td colspan="3">Halides</td><td>F-, Cl-</td><td>Halite, Fluorite</td>
            </tr>
            <tr>
                <td colspan="3">Hydroxides</td><td>(OH)-</td><td>Bauxite</td>
            </tr>
            <tr>
                <td colspan="3">Phosphates</td><td>PO4-</td><td>Apatite</td>
            </tr>
        </tbody>
    </table>
    """

    st.markdown(html, unsafe_allow_html=True)

with tab3:

    st.header("Crystal Systems")

    with st.expander("**Cubic**"):
        st.write(
            "Three equal and perpendicular axes, forming perfect cubes. Also called isometric. Ex.: Pyrite, Diamond, Galena."
        )
        cols = st.columns(3)
        with cols[0]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2018/02/Pirita-6-400x400.jpg",
                width=200,
                caption="**Pyrite**",
            )
        with cols[1]:
            st.image("assets/cristalinos/cubico.png", width=200)
        with cols[2]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2018/02/Galena-2-400x400.jpg",
                width=200,
                caption="**Galena**",
            )

    with st.expander("**Monoclinic**"):
        st.write("Three unequal axes, two perpendicular and one inclined. Ex.: Gypsum.")
        cols = st.columns(3, gap="medium")
        with cols[0]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2017/09/Gipsita_2-400x400.jpg",
                width=200,
                caption="**Gypsum**",
            )
        with cols[1]:
            st.image("assets/cristalinos/monoclinico.png", width=200)
        with cols[2]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2017/09/Gipsita_6-400x400.jpg",
                width=200,
                caption="**Gypsum**",
            )

    with st.expander("**Triclinic**"):
        st.write(
            "Three unequal and inclined axes, with no right angles. Ex.: Turquoise."
        )
        cols = st.columns(3)
        with cols[0]:
            st.image(
                "https://kaviah.com/wp-content/uploads/2021/02/turquesa-capa.jpg",
                width=200,
                caption="**Turquoise**",
            )
        with cols[1]:
            st.image("assets/cristalinos/triclinico.png", width=200)
        with cols[2]:
            st.image(
                "https://i0.wp.com/geologyscience.com/wp-content/uploads/2019/07/Turquoise-pyrite-quartz.jpeg?resize=640%2C425&ssl=1",
                width=200,
                caption="**Turquoise**",
            )

    with st.expander("**Orthorhombic**"):
        st.write("Three unequal axes, all perpendicular to each other. Ex.: Topaz.")
        cols = st.columns(3)
        with cols[0]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2019/01/Topazio-16-400x400.jpg",
                width=200,
                caption="**Topaz**",
            )
        with cols[1]:
            st.image("assets/cristalinos/ortorrombico.png", width=200)
        with cols[2]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2018/02/Top%C3%A1zio-2-400x400.jpg",
                width=200,
                caption="**Topaz**",
            )

    with st.expander("**Rhombohedral**"):
        st.write(
            "Three equal axes with equal angles but different from 90°. Ex.: Calcite."
        )
        cols = st.columns(3)
        with cols[0]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2019/02/Calcita-17-400x400.jpg",
                width=200,
                caption="**Calcite**",
            )
        with cols[1]:
            st.image("assets/cristalinos/romboedrico.png", width=200)
        with cols[2]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2019/02/Calcita-16-400x400.jpg",
                width=200,
                caption="**Calcite**",
            )

    with st.expander("**Tetragonal**"):
        st.write("Two equal axes, one different, all perpendicular. Ex.: Zircon.")
        cols = st.columns(3)
        with cols[0]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2020/03/zircao-1-400x400.jpg",
                width=200,
                caption="**Zircon**",
            )
        with cols[1]:
            st.image("assets/cristalinos/tetragonal.png", width=200)
        with cols[2]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2020/03/zircao-2-400x400.jpg",
                width=200,
                caption="**Zircon**",
            )

    with st.expander("**Hexagonal**"):
        st.write(
            "Two equal axes at 120°, and one different axis perpendicular to them. Ex.: Beryl."
        )
        cols = st.columns(3)
        with cols[0]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2019/02/Berilo-26-400x400.jpg",
                width=200,
                caption="**Beryl**",
            )
        with cols[1]:
            st.image("assets/cristalinos/hexagonal.png", width=200)
        with cols[2]:
            st.image(
                "https://museuhe.com.br/site/wp-content/uploads/2019/02/Berilo-27-400x400.jpg",
                width=200,
                caption="**Beryl**",
            )

    st.header("Crystal System Viewer")

    type = st.pills(
        label="Choose a crystal system:",
        default="Cubic",
        options=[
            "Cubic",
            "Tetragonal",
            "Orthorhombic",
            "Hexagonal",
            "Triclinic",
            "Monoclinic",
            "Rhombohedral",
        ],
    )

    fig = generate_crystal(type)
    st.plotly_chart(fig)

with tab4:
    st.header("Hardness")

    html_dureza = """
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: center;">
        <thead style="background:#bc1077">
            <tr>
                <th>Hardness Value</th>
                <th>Example Mineral</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Talc</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Gypsum</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Calcite</td>
            </tr>
            <tr>
                <td>4</td>
                <td>Fluorite</td>
            </tr>
            <tr>
                <td>5</td>
                <td>Apatite</td>
            </tr>
            <tr>
                <td>6</td>
                <td>Feldspar</td>
            </tr>
            <tr>
                <td>7</td>
                <td>Quartz</td>
            </tr>
            <tr>
                <td>8</td>
                <td>Topaz</td>
            </tr>
            <tr>
                <td>9</td>
                <td>Corundum</td>
            </tr>
            <tr>
                <td>10</td>
                <td>Diamond</td>
            </tr>
        </tbody>
    </table>
    """

    st.markdown(html_dureza, unsafe_allow_html=True)

with tab5:
    st.header("Mineral Identifier")
    st.info(
        """
        This section is not yet available in English. 
        It is a work in progress. Meanwhile, 
        you can use your browser's translator 
        to access the content.
        """,
        icon=":material/priority_high:",
    )
    st.write("Escolha as propriedades observadas:")
    st.divider()

    mineral_id.run()
