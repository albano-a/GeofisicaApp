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
        Uma das formas mais conhecidas de Calculate a saturação de água é por meio da equação de Archie, que pode ser utilizada tanto para a resistividade quanto para a resistividade aparente. A diferença entre as duas equações é que na de resistividade se usa a resistividade da formação, e na de resistividade aparente se usa a resistividade verdadeira da formação, conseguido a partir de um perfil de resistividade profunda.
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
            phi = st.number_input(r"$\phi$ (decimal)", min_value=0.01, max_value=1.00)
            a = st.number_input(
                "$a$",
                min_value=0.01,
                help="Grau de desvio das trajetórias dos fluidos em relação ao caminho mais curto, devido à geometria dos poros.",
                key="fator_tortuosidade_1",
            )
        if st.button("Calculate", key=4):
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
                st.warning(f"An error occurred: {e}")

    with st.expander("Resistividade da Água - Western Atlas (1985)"):
        st.write(
            r"""
            A Western Atlas (1985) propôs uma equação para o cálculo da resistividade da água ($R_w$), composta por expressões matemáticas e valores como a resistividade equivalente da água ($R_{we}$) e a temperatura no fundo do poço ($\text{BHT}$). A equação é a seguinte:
            """
        )
        st.latex(
            r"R_{w} = \frac{ R_{we} + 0.131 \cdot 10 ^ {\left(\frac{1}{\log(\text{BHT}/19.9)} - 2 \right)} }{ -0.5 \cdot R_{we} + 10 ^ {\left(\frac{0.0426}{\log(\text{BHT}/50.8)}\right)} }"
        )

        cols = st.columns(2)
        with cols[0]:
            rwe = st.number_input("$R_{we} $ (ohm-m)", min_value=0.00)
        with cols[1]:
            bht = st.number_input(r"$\text{BHT}$ (ºF)", min_value=0.00)

        if st.button("Calculate", key="western_atlas_1"):
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
                st.warning(f"An error occurred: {e}")

        list_western_atlas_tabs = [
            r"Res. Equivalente da Água ($R_{we}$)",
            r"Res. do Filtrado de Lama ($R_{mf}$)",
            r"Temperatura da Formação ($T_{f}$)",
        ]

        wes_at_tabs = st.tabs(list_western_atlas_tabs)

        with wes_at_tabs[0]:
            st.latex(r"R_{we} = R_{mf} \cdot 10^{ {SP}/{61 + 0.133\text{BHT}}}")
            st.write(
                r"""
                $R_{mf}$ - Resistividade do Filtrado de Lama na Temperatura da Formação  
                $\text{BHT}$ - Temperatura no Fundo do Poço (Bottom Hole Temperature)  
                $SP$ - Medida do Potencial Espontâneo
                """
            )
            cols = st.columns(3)
            with cols[0]:
                rmf = st.number_input("$R_{mf}$ (ohm-m)", min_value=0.00, key="rmf_rwe")
            with cols[1]:
                bht = st.number_input(
                    r"$\text{BHT}$ (ºF)", min_value=0.00, key="bht_rwe"
                )
            with cols[2]:
                sp = st.number_input("$SP$ (mV)", min_value=0.00, key="sp_rwe")

            if st.button("Calculate", key="western_atlas_2"):
                try:
                    rwe = rmf * 10 ** (sp / (61 + 0.133 * bht))
                    st.metric(
                        "Resistividade Equivalente da Água", value=f"{rwe:.4f} ohm-m"
                    )
                except Exception as e:
                    st.warning(f"An error occurred: {e}")

        with wes_at_tabs[1]:
            st.latex(r"R_{mf} = \frac{R_{mfsurf}(T_{surf}+6.77)}{T_{f} + 6.77}")
            st.write(
                r"""
                $R_{mf}$ - Resistividade do filtrado de lama na temperatura da formação
                $R_{mfsurf}$ - Resistividade do filtrado de lama na temperatura medida
                $T_{surf}$ - Temperatura na qual a R_{mf} foi medida (temperatura superficial)
                $T_{f}$ - Temperatura da Formação
                """
            )
            cols = st.columns(3)
            with cols[0]:
                rmfsurf = st.number_input(
                    "$R_{mfsurf}$ (ohm-m)", min_value=0.00, key="rmfsurf_rmf"
                )
            with cols[1]:
                tsurf = st.number_input(
                    r"$T_{surf}$ (ºC)", min_value=0.00, key="tsurf_rmf"
                )
            with cols[2]:
                tf = st.number_input("$SP$ (mV)", min_value=0.00, key="tf_rmf")

            if st.button("Calculate", key="wester_atlas_3"):
                try:
                    rmf = (rmfsurf * (tsurf + 6.77)) / (tf + 6.77)
                    st.metric(
                        "Resistividade Equivalente da Água", value=f"{rmf:.4f} ohm-m"
                    )
                except Exception as e:
                    st.warning(f"An error occurred: {e}")
        with wes_at_tabs[2]:
            st.latex(r"T_{f} = \left(\frac{BHT - AMST}{TD} \cdot FD \right) + AMST")
            st.write(
                """
                $AMST$ - Temperatura Superficial Anual Média  
                $TD$ - Profundidade Total  
                $BHT$ - Temperatura no Fundo do Poço  
                $T_{f}$ - Temperatura da Formação  
                $FD$ - Profundidade da Formação  
                """
            )
            cols = st.columns(2)

            with cols[0]:
                bht = st.number_input(r"$\text{BHT}$ (ºF)", key="bht_tf")
                td = st.number_input(r"$TD$ (ft)", min_value=0.00)
            with cols[1]:
                amst = st.number_input(r"$AMST$ (ºF)")
                fd = st.number_input(r"$FD$ ft", min_value=0.00)

            if st.button("Calculate", key="calculate_tf"):
                try:
                    tf = ((bht - amst) / td * fd) + amst
                    st.metric("Temperatura de Formação", value=f"{tf:.2f} ºF")
                except:
                    print("An exception occurred")

    with st.expander("Resistividade da Água - Perfil SP"):
        st.write(
            """
            Resistividade da água (Rw) também pode ser calculada a partir do registro de potencial espontâneo (SP) do poço. Essa equação requer os valores da resistividade do filtrado de lama, uma medição de SP e uma constante K que depende da temperatura da formação. A equação é a seguinte:
            """
        )
        st.latex(r"R_w = 10^{(K \cdot \log(R_{mf}) + SP) / K}")
        st.write(
            r"""
            Onde:
            $R_{w}$ - Resistividade da Água
            $R_{mf}$ - Resistividade do Filtrado de Lama na Temperatura da Formação
            $K$ - Constante
            $SP$ - Potencial Espontâneo
            """
        )
        cols = st.columns(3)
        with cols[0]:
            k_input = st.number_input("$K$", min_value=0.00)
        with cols[1]:
            rmf_input = st.number_input("$R_{mf}$", min_value=0.01)
        with cols[2]:
            sp_input = st.number_input("$SP$", min_value=0.00)

        if st.button("Calculate", key="sp-log"):
            k = k_input
            rmf = rmf_input
            sp = sp_input
            try:
                rw_output = 10 ** ((k * np.log10(rmf) + sp) / k)
                st.metric("Resistividade da Água", value=f"{rw_output:.4f} ohm-m")
            except Exception as e:
                st.error(f"Um erro ocorreu: {e}")

        k_tab = st.tabs(["Constante $K$"])
        with k_tab[0]:
            st.write(
                """
                Para o cálculo da constante K, é necessário conhecer a temperatura da formação, e a expressão é a seguinte:
                """
            )
            st.latex(r"K = (0.133 \cdot T_{f}) + 60")
            st.write("$T_{f}$ - Temperatura da Formação")

            cols = st.columns(3)
            with cols[1]:
                tf = st.number_input("$T_{f} (ºF)$", min_value=0.00)

            if st.button("Calculate", key="sp-log-tf"):
                try:
                    K = (0.133 * tf) + 60
                    st.metric("Constante K", value=f"{K}")
                except:
                    print("An exception occurred")

    with st.expander("Resistividade Total"):
        st.write(
            r"""
            A resistividade total ($R_t$) pode ser calculada pela equação de Archie. Essa equação é composta pelos valores de resistividade da água ($R_w$), fator de tortuosidade ($a$), porosidade ($\phi$), e os expoentes de cementação ($m$) e saturação ($n$). A expressão é a seguinte:
            """
        )
        st.latex(r"R_{t} = \frac{ a \cdot R_{w} }{ \phi^{m} \cdot S_{w}^{n}}")

        cols = st.columns(3)
        with cols[0]:
            rw = st.number_input("$R_{w}$", min_value=0.00)
            a = st.number_input("$a$", min_value=0.00)
        with cols[1]:
            phi = st.number_input(r"$\phi$", min_value=0.00)
            m = st.number_input("$m$", min_value=0.00)
        with cols[2]:
            sw = st.number_input("$S_{w}$", min_value=0.00)
            n = st.number_input("$n$", min_value=0.00)

        if st.button("Calculate", key="total_resistivity"):
            try:
                rt = (a * rw) / ((phi**m) * (sw**n))
                st.metric("Resistividade Total", value=f"{rt:.4f}")
            except Exception as e:
                st.error(f"Um erro ocorreu: {e}")
