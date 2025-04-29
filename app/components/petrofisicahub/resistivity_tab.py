import streamlit as st
import numpy as np


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

    with st.expander(r"Resistividade da Água $R_{w}$/$R_{wa}$ - Archie"):
        st.write(
            r"""
        Uma das formas mais conhecidas de calcular a saturação de água é por meio da equação de Archie, que pode ser utilizada tanto para a resistividade quanto para a resistividade aparente. A diferença entre as duas equações é que na de resistividade se usa a resistividade da formação, e na de resistividade aparente se usa a resistividade verdadeira da formação, conseguido a partir de um perfil de resistividade profunda.
        """
        )
        st.latex(
            r"""
            R_{w} = \frac{R_{o} \cdot \phi^{m}}{a}\space\text{ou}\space R_{wa} = \frac{R_{t} \cdot \phi^{m}}{a}
                 """
        )
        st.write(
            r"""
         Onde:
            - $R_w/R_{wa}$ - Resistividade da Água/Resistividade Aparente da Água
                        
            - $R_{o}$ - Resistividade da formação saturada com água
            
            - $R_{t}$ - Resistividade verdadeira da formação obtida a partir de um perfil de resistividade profunda

            - $\phi$ - Porosidade / $m$ - Expoente de cimentação / $a$ - Fator de tortuosidade

        """
        )
        list_rest_opts = [
            r"Resistividade - $R_w$",
            r"Resistividade Aparente - $R_{wa}$",
        ]
        res_opts = st.radio(
            "Tipo",
            [r"Resistividade - $R_w$", r"Resistividade Aparente - $R_{wa}$"],
            horizontal=True,
        )
        cols = st.columns(2)
        with cols[0]:
            ro = st.number_input(
                "$R_o$ (ohm-m)" if res_opts == list_rest_opts[0] else "$R_t$ (ohm-m)",
                min_value=0.0,
            )
            m = st.number_input(
                "$m$",
                min_value=0.0,
                help="Reflete a compactação e a permeabilidade da rocha.",
                key="expoente_cimentacao_1",
            )
        with cols[1]:
            phi = st.number_input("$\phi$ (decimal)", min_value=0.01, max_value=1.00)
            a = st.number_input(
                "$a$",
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
                    st.metric(
                        (
                            "Resistividade da Água"
                            if res_opts == list_rest_opts[0]
                            else "Resistividade Aparente da Água"
                        ),
                        value=f"{rw:.4f} ohm-m",
                    )
            except Exception as e:
                st.warning(f"Ocorreu um erro: {e}")

    with st.expander("Resistividade da Água - Western Atlas (1985)"):
        st.write(
            r"""
            A Western Atlas (1985) propôs uma equação para o cálculo da resistividade da água ($R_w$), composta por expressões matemáticas e valores como a resistividade equivalente da água ($R_{we}$) e a temperatura no fundo do poço ($\text{BHT}$). A equação é a seguinte:
            """
        )
        st.latex(
            r"R_{w} = \frac{ R_{we} + 0.131 \cdot 10 ^ {(\frac{1}{\log(\text{BHT}/19.9)} - 2)} }{ -0.5 \cdot R_{we} + 10 ^ {(\frac{0.0426}{\log(\text{BHT}/50.8)})} }"
        )

        cols = st.columns(2)
        with cols[0]:
            rwe = st.number_input("$R_{we} $ (ohm-m)", min_value=0.00)
        with cols[1]:
            bht = st.number_input(r"$\text{BHT}$ (ºF)", min_value=0.00)

        if st.button("Calcular", key="western_atlas_1"):
            try:
                if a == 0:
                    st.warning("O fator de tortuosidade não pode ser zero.")
                else:
                    rw = (rwe + 0.131 * 10 ** ((1 / (np.log10(bht / 19.9))) - 2)) / (
                        -0.5 * rwe + 10 ** (0.0426 / np.log10(bht / 50.8))
                    )
                    if rw < 0:
                        st.error("Algo está errado, o resultado não pode ser negativo.")
                    else:
                        st.metric(
                            "Resistividade da Água",
                            value=f"{rw:.4f} ohm-m",
                        )
            except Exception as e:
                st.warning(f"Ocorreu um erro: {e}")

        list_western_atlas_tabs = [
            r"Resistividade Equivalente da Água ($R_{we}$)",
            r"Resistividade do Filtrado de Lama ($R_{mf}$)",
            r"Temperatura da Formação ($T_{f}$)",
        ]
        
        wes_at_tabs = st.tabs(list_western_atlas_tabs)
        
        with wes_at_tabs[0]:
            st.latex(
                r"R_{we} = R_{mf} \cdot 10^{ {SP}/{61 + 0.133\text{BHT}}}"
            )
            st.write(
                """
                - $R_{mf}$ - Resistividade do Filtrado de Lama na Temperatura da Formação
                - $\text{BHT}$ - Temperatura no Fundo do Poço
                - $SP$ - Medida do Potencial Espontâneo
                """
            )
            
        with wes_at_tabs[1]:
            st.write()
        with wes_at_tabs[2]:
            st.write()
            
            
