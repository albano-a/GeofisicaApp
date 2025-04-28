import streamlit as st


def render_water_saturation():
    st.subheader("Saturação de Água")

    with st.expander("Saturação de Água (Sw) - Archie (1942)"):
        st.write(
            """
        A equação de Archie é uma das formas mais conhecidas de calcular a saturação de água. O autor incluiu diferentes propriedades físicas da rocha e medições de logs de poço, como tortuosidade, resistividade da água e da formação, expoente de saturação e porosidade. A equação é a seguinte: 
        """
        )
        st.latex(
            r"S_{w} = \left(\frac{  a \cdot R_{w}  }{ R_{t} \cdot \phi^{m} }  \right)^{\frac{1}{n}}"
        )
        st.write(
            r"""
            Onde:

            - $S_{w}$ - Saturação de água da zona não invasada

            - $R_{t}$ - Resistividade verdadeira da formação (ou seja, indução profunda ou laterolog corrigido para invasão)

            - $R_{w}$ - Resistividade da água da formação na temperatura da formação

            - $\phi$ - Porosidade

            - $a$ - Fator de tortuosidade

            - $m$ - Expoente de cimentação

            - $n$ - Expoente de saturação
            """
        )
        cols = st.columns(2)
        with cols[0]:
            a = st.number_input(
                "Fator de Tortuosidade ",
                min_value=0.01,
                help="Grau de desvio das trajetórias dos fluidos em relação ao caminho mais curto.",
                key="fator_tortuosidade_2",
            )
            rt = st.number_input(
                "Resistividade verdadeira da Formação (ohm-m)",
                min_value=0.0,
                help="Resistividade verdadeira da formação (ou seja, indução profunda ou laterolog corrigido para invasão).",
            )
            m = st.number_input(
                "Expoente de Cimentação ",
                min_value=0.0,
                help="Reflete a compactação e a permeabilidade da rocha.",
                key="expoente_cimentacao_2",
            )
        with cols[1]:
            rw_in = st.number_input(
                "Resistividade da Água da Formação (ohm-m)",
                min_value=0.0,
                help="Resistividade da água da formação na temperatura da formação",
            )
            phi = st.number_input(
                "Porosidade (decimal)",
                min_value=0.01,
                max_value=1.00,
                key="porosidade_5",
            )
            n = st.number_input(
                "Expoente de Saturação",
                min_value=0.0,
                help="Ajusta a relação entre resistividade e saturação.",
            )
        if st.button("Calcular", key=5):
            try:
                if a == 0:
                    st.warning("O fator de tortuosidade não pode ser zero.")
                else:
                    sw_archie = ((a * rw_in) / (rt * (phi**m))) ** (1 / n)
                    st.success(
                        f"Saturação de água calculada: {sw_archie:.4f} | {sw_archie*100:.2f}%"
                    )
            except:
                print("An exception occurred")
