import streamlit as st
import scripts.petrophysics.shale_volume as sv


def render_shale_volume():
    st.subheader("Volume de Shale")

    st.write(
        """
        O volume de argila (shale) é um valor fundamental para avaliar a qualidade de uma rocha reservatório. De acordo com o volume de argila que uma rocha reservatório possui, será determinado o quão explorável um reservatório é.

        Existem diferentes métodos para calcular o volume de argila: Larionov, Larionov-rochas antigas, Steiber, Clavier. Algumas dessas equações utilizam os valores de registro de poço de gamma ray, e algumas delas utilizam valores da ferramenta de registro de potencial espontâneo (SP).

        Além disso, esse valor é usado para fazer correção de argila para valores de porosidade derivados de diferentes ferramentas de registro de poços, para que se possa ter um valor de porosidade mais confiável. 
        """
    )

    with st.expander("Índice de GR"):
        st.write(
            """
        O **Índice de Gamma Ray (IGR)** é calculado a partir da ferramenta de perfil geofísico que tem o mesmo nome. Esse índice leva em consideração o valor mínimo de gamma ray (zona mais limpa), o valor máximo de gamma ray (zona mais argilosa) e o valor da área ou profundidade de estudo. 
        """
        )
        st.latex(r"I_{GR}=\frac{ GR_{log} - GR_{min} }{ GR_{max} - GR_{min} }")
        st.write(
            r"""
         Onde:  
        - $I_{GR}$ - Índice de gamma ray  
        - $GR_{log}$ - Leitura de gamma ray da formação  
        - $GR_{min}$ - Valor mínimo de gamma ray (areia limpa ou carbonato)  
        - $GR_{max}$ - Valor máximo de gamma ray (argila)  
        
        O Índice de gamma ray é o ponto de partida para calcular o volume de argila a partir de diferentes equações de diversos autores.
        """
        )
        gr_log = st.number_input(
            r"$\text{GR}_{log}$ (API)", min_value=0.0, max_value=250.0, format="%1f"
        )
        cols = st.columns(2)
        with cols[0]:
            gr_min = st.number_input(
                r"$\text{GR}_{min}$ (API)", min_value=0.0, max_value=250.0, format="%1f"
            )
        with cols[1]:
            gr_max = st.number_input(
                r"$\text{GR}_{max}$ (API)", min_value=0.0, max_value=250.0, format="%1f"
            )

        if st.button("Calcular IGR"):
            try:
                if gr_max == gr_min:
                    st.warning("GR_max e GR_min não podem ser iguais.")
                else:
                    igr = (gr_log - gr_min) / (gr_max - gr_min)
                    st.metric(
                        label="Índice de Gamma Ray", value=f"{igr:.4g} | {igr*100:.2f}%"
                    )
            except Exception as e:
                st.warning(f"Ocorreu um erro: {e}")

    with st.expander("Larionov (1969)"):
        tab1, tab2 = st.tabs(["Larionov", "Larionov Old Rocks"])
        with tab1:
            st.write(
                """
                A equação de Larionov (1969) para rochas do Cenozóico (anteriormente conhecidas como rochas terciárias) utilizada para o cálculo do volume de argila é a seguinte:
                """
            )
            st.latex(r"V_{sh} = 0.083 \cdot (2^{3.7 \cdot I_{GR}} - 1)")
            st.write(
                r"""
                Onde:  
                $I_{GR}$ - Índice de gamma ray  
                $V_{sh}$ - Volume de argila  
                """
            )
            cols = st.columns(3)
            with cols[1]:
                igr = st.number_input(
                    r"$I_{GR}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="igr_larionov",
                )
            if st.button("Calcular", key="larionov"):
                try:
                    vsh = sv.larionov(igr)
                    st.metric(
                        label="Volume de Shale",
                        value=f"{vsh:.4g} | {vsh*100:.2f}%",
                    )
                except Exception as e:
                    st.warning("Alguma coisa deu errado: {e}")

        with tab2:
            st.write(
                """
            Larionov (1969) também propôs uma equação para o cálculo do volume de argila em rochas mais antigas que a Era Cenozóica, expressa da seguinte forma:
            """
            )
            st.latex(r"V_{sh} = 0.33 \cdot (2^{2 \cdot I_{GR}} - 1)")
            st.write(
                r"""
                Onde:  
                $I_{GR}$ - Índice de gamma ray  
                $V_{sh}$ - Volume de argila  
                """
            )
            cols = st.columns(3)
            with cols[1]:
                igr = st.number_input(
                    r"$I_{GR}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="igr_larionov_old_rocks",
                )
            if st.button("Calcular", key="larionov_old_rocks"):
                try:
                    if igr <= 1.00 and igr > 0.00:
                        vsh = sv.larionov_old_rocks(igr)
                        st.metric(
                            label="Volume de Shale",
                            value=f"{vsh:.4g} | {vsh*100:.2f}%",
                        )
                    else:
                        st.warning(r"$I_{GR}$ deve ser maior que 0 e menor que 1")
                except Exception as e:
                    st.warning("Alguma coisa deu errado: {e}")

    with st.expander("Steiber (1970)"):
        st.write(
            """
            Steiber (1970) também propôs uma equação para o cálculo do volume de argila, expressa da seguinte forma:
            """
        )
        st.latex(
            r"""
            V_{sh} = \frac{I_{GR}}{3 - 2 \cdot I_{GR}}
            """
        )
        st.write(
            r"""
            Onde:  
            $I_{GR}$ - Índice de gamma ray  
            $V_{sh}$ - Volume de argila  
            """
        )
        cols = st.columns(3)
        with cols[1]:
            igr = st.number_input(
                r"$I_{GR}$ (decimal)",
                min_value=0.00,
                max_value=1.00,
                key="igr_steiber",
            )
        if st.button("Calcular", key="steiber"):
            try:
                if igr <= 1.00 and igr > 0.00:
                    vsh = sv.steiber(igr)
                    st.metric(
                        label="Volume de Shale",
                        value=f"{vsh:.4g} | {vsh*100:.2f}%",
                    )
                else:
                    st.warning(r"$I_{GR}$ deve ser maior que 0 e menor que 1")
            except Exception as e:
                st.warning("Alguma coisa deu errado: {e}")

    with st.expander("Clavier (1971)"):
        st.write(
            """
            Clavier (1971) propôs uma equação para o cálculo do volume de argila, com uma expressão mais complexa em comparação a outros autores, apresentada da seguinte forma:
            """
        )
        st.latex(
            r"""
            V_{sh} = 1.7 - [3.38 - (I_{GR} + 0.7)^{2}]^{\frac{1}{2}}
            """
        )
        st.write(
            r"""
            Onde:  
            $I_{GR}$ - Índice de gamma ray  
            $V_{sh}$ - Volume de argila  
            """
        )
        cols = st.columns(3)
        with cols[1]:
            igr = st.number_input(
                r"$I_{GR}$ (decimal)",
                min_value=0.00,
                max_value=1.00,
                key="igr_clavier",
            )
        if st.button("Calcular", key="clavier"):
            try:
                if igr <= 1.00 and igr > 0.00:
                    vsh = sv.clavier(igr)
                    st.metric(
                        label="Volume de Shale",
                        value=f"{vsh:.4g} | {vsh*100:.2f}%",
                    )
                else:
                    st.warning(r"$I_{GR}$ deve ser maior que 0 e menor que 1")
            except Exception as e:
                st.warning("Alguma coisa deu errado: {e}")

    with st.expander("Shale Volume - SP"):
        tab1, tab2 = st.tabs(["Clássica", "Alternativa"])
        with tab1:
            st.write(
                """
                A partir do perfil de potencial espontâneo (SP), é possível calcular o volume de argila utilizando duas equações diferentes. A primeira expressão é a seguinte:
                """
            )
            st.latex(
                r"""
                V_{sh} = 1 - \frac{PSP}{SSP}
                """
            )
            st.write(
                r"""
                Onde:  
                $V_{sh}$ - Volume de argila  
                $PSP$ - Potencial espontâneo pseudostático (máximo SP da formação argilosa)  
                $SSP$ - Potencial espontâneo estático de uma camada arenítica limpa e espessa próxima  
                """
            )
            cols = st.columns(2)
            with cols[0]:
                psp = st.number_input(
                    r"$PSP$ (mV)",
                    min_value=0.00,
                    key="psp_sp",
                )
            with cols[1]:
                ssp = st.number_input(
                    r"$SSP$ (mV)",
                    min_value=0.00,
                    key="ssp_sp",
                )
            if st.button("Calcular", key="sp"):
                try:

                    vsh = 1 - (psp / ssp)
                    if 0 < vsh < 1:
                        st.metric(
                            label="Volume de Shale",
                            value=f"{vsh:.4g} | {vsh*100:.2f}%",
                        )
                    else:
                        st.error(
                            "O resultado não deve ser superior a 100% nem negativo. Verifique seus valores."
                        )

                except Exception as e:
                    st.warning("Alguma coisa deu errado: {e}")
        with tab2:
            st.write(
                "A outra forma de calcular o volume de shale é seguindo essa outra equação:"
            )
            st.latex(r"V_{sh} = \frac{PSP - SSP}{SP_{shale} - SSP}")
            st.write(
                r"""Onde:  
                        $SP_{shale}$ - Valor do SP em uma argila (normalmente é zero)"""
            )
            cols = st.columns(3)
            with cols[0]:
                psp = st.number_input(
                    r"$PSP$ (mV)",
                    min_value=0.00,
                    key="psp_sp_shale",
                )
            with cols[1]:
                ssp = st.number_input(
                    r"$SSP$ (mV)",
                    min_value=0.00,
                    key="ssp_sp_shale",
                )
            with cols[2]:
                sp_shale = st.number_input(
                    r"$SSP$ (mV)",
                    min_value=0.00,
                    key="sp_shale_shale",
                )
            if st.button("Calcular", key="sp_shale"):
                try:
                    # O resultado não deve ser superior a 100% nem negativo. Verifique seus valores.
                    vsh = (psp - ssp) / (sp_shale - ssp)
                    if 0 < vsh < 1:
                        st.metric(
                            label="Volume de Shale",
                            value=f"{vsh:.4g} | {vsh*100:.2f}%",
                        )
                    else:
                        st.error(
                            "O resultado não deve ser superior a 100% nem negativo. Verifique seus valores."
                        )
                except Exception as e:
                    st.warning("Alguma coisa deu errado: {e}")

    with st.expander("Todas as equações"):

        igr = st.slider(r"$I_{GR} (decimal)$", min_value=0.0, max_value=1.0)
        # igr = st.number_input(r"$I_{GR} (decimal)$")

        try:
            fig = sv.plot_igr(igr_custom=igr)
            st.pyplot(fig)
        except ValueError as ve:
            st.warning(f"Erro: {ve}")
