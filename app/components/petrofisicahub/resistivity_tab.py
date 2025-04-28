import streamlit as st


def render_resistivity():
    st.subheader("Resistividade")

    st.write(
        """
        Resistividade é definida como a oposição ou resistência que um material tem para interferir no 
        fluxo de uma corrente elétrica. No caso das rochas sedimentares, estas contêm fluidos em seus 
        poros que têm diferentes tipos de resistividades.

        Um volume de poros da rocha pode conter igualmente óleo, gás ou água. Óleo e gás têm um valor 
        de resistividade mais alto do que a água, o que permite detectar a presença de hidrocarbonetos 
        em um poço usando ferramentas de registro de resistividade, por exemplo.

        No entanto, a salinidade da água também afeta a resistividade da água, e ela pode ter uma ampla 
        gama de valores. A água salgada tem uma resistividade menor do que a água doce, portanto, tem um 
        valor de resistividade mais baixo.

        Além de ajudar a detectar a presença de hidrocarbonetos, a resistividade da água é amplamente 
        utilizada para o cálculo da saturação de água, que é um valor muito importante na 
        estimativa de reservas de hidrocarbonetos. 
        """
    )

    with st.expander("Resistividade da Água Rw - Archie"):
        st.write(
            """
         Uma das formas mais conhecidas de calcular a saturação de água é por meio da equação de Archie. 
         Essa equação leva em consideração medições e valores como a resistividade da formação saturada com água, 
         porosidade, fator de tortuosidade e o expoente de cimentação. A equação expressa é a seguinte:
        """
        )
        st.latex(
            r"""
            R_{w} = \frac{R_{o} \cdot \phi^{m}}{a}
                 """
        )
        st.write(
            r"""
         Onde:

            - $R_{o}$ - Resistividade da formação saturada com água

            - $\phi$ - Porosidade
            
            - $m$ - Expoente de cimentação

            - $a$ - Fator de tortuosidade

        """
        )
        cols = st.columns(2)
        with cols[0]:
            ro = st.number_input(
                "Resistividade de Formação (ohm-m)",
                min_value=0.0,
                help="Resistividade de Formação da Água Saturada",
            )
            m = st.number_input(
                "Expoente de Cimentação",
                min_value=0.0,
                help="Reflete a compactação e a permeabilidade da rocha.",
                key="expoente_cimentacao_1",
            )
        with cols[1]:
            phi = st.number_input(
                "Porosidade (decimal)", min_value=0.01, max_value=1.00
            )
            a = st.number_input(
                "Fator de Tortuosidade",
                min_value=0.01,
                help="Grau de desvio das trajetórias dos fluidos em relação ao caminho mais curto, devido à geometria dos poros.",
                key="fator_tortuosidade_1",
            )
        if st.button("Calcular", key=4):
            try:
                if a == 0:
                    st.warning("O fator de tortuosidade não pode ser zero.")
                else:
                    rw = (ro * phi**m) / a
                    st.success(f"Resistividade da água calculada: {rw:.4f} ohm-m")
            except Exception as e:
                st.warning(f"Ocorreu um erro: {e}")
