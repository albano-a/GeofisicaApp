import streamlit as st
import scripts.petrophysics.porosity as porosity
import scripts.petrophysics.shale_volume as sv


def render_permeability():
    st.subheader("Permeabilidade")

    st.write(
        """
        Permeabilidade é a facilidade com que um fluido flui através de um meio poroso. Definida por Darcy, é medida em unidades que levam seu nome. É usada para diferenciar reservatórios convencionais de não convencionais, dependendo do fluido produzido (óleo ou gás).

        A permeabilidade é geralmente calculada em laboratório, testando uma amostra de rocha com diferentes técnicas. Contudo, as medições podem ser imprecisas devido às mudanças nas condições das rochas após a extração.

        Diversas equações foram propostas para calcular a permeabilidade, mas as medições laboratoriais ainda são as mais precisas. Também existem estimativas derivadas de registros de poços por ressonância magnética nuclear (NMR), usadas por algumas empresas para determinar porosidade efetiva a partir do conteúdo de hidrogênio.

        A escolha entre dados laboratoriais ou estimativas derivadas de equações depende do critério do petrofísico ou do especialista em reservatórios.
        """
    )

    with st.expander(
        "Permeabilidade - Wyllie & Rose (1950) - Óleo de Média Densidade",
        icon=":material/landslide:",
    ):
        st.write(
            """
        Wyllie & Rose (1950) desenvolveram uma equação para calcular a permeabilidade em reservatórios de óleos de média densidade. Essa equação leva em consideração os valores de porosidade e saturação de água irredutível, e a expressão é a seguinte: 
        """
        )
        st.latex(r"K = (250 \cdot \frac{\phi^{3}}{Swirr})^{2}")
        st.write(
            r"""
        Onde:  
        - K - Permeabilidade em milidarcy  
        - $\phi$ - Porosidade  
        - Swirr - Saturação de água (Sw) de uma zona com saturação irredutível de água
        """
        )
        cols = st.columns(2)
        with cols[0]:
            phi = st.number_input("Porosidade (decimal)")
        with cols[1]:
            swirr = st.number_input(
                "Saturação de Água em uma zona irredutível (decimal)",
                min_value=0.01,
                max_value=1.00,
            )
        if st.button("Calcular", key=3):
            try:
                K = (250 * ((phi**3) / swirr)) ** 2
                st.success(f"Resultado (mD): {K:.4f}")
            except Exception as e:
                st.warning(f"Ocorreu um erro: {e}")
