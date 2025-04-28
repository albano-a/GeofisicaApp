import streamlit as st


def render_oil_reserves():
    st.subheader("Reservas")
    st.write(
        """
    O cálculo da porosidade e da saturação de água desempenha um papel importante no momento de estimar
    as reservas de petróleo e gás, pois um erro considerável ao calcular esses dois valores pode trazer
    sérios problemas econômicos se estivermos falando de um reservatório gigante.

    O fator de recuperação é outro parâmetro importante nos cálculos de estimativa de reservas, e esse
    valor dependerá do(s) mecanismo(s) de drenagem natural do reservatório (capa de gás, aquífero, etc.),
    que são muito diferentes entre eles. Além disso, o fator de recuperação pode aumentar com a aplicação
    de técnicas de recuperação secundária e terciária no reservatório, mas essa melhoria adiciona mais custos
    ao orçamento de exploração.  
    """
    )
    with st.expander("Óleo/Petróleo"):
        list_of_reserves_tabs = [
            "Reservas de Petróleo",
            "Fator de Volume de Óleo",
            "Razão Óleo-Gás",
        ]

        reserve_tabs = st.tabs(list_of_reserves_tabs)

        with reserve_tabs[0]:
            st.latex(
                r"N_{f} = \frac{7758 \cdot A \cdot h \cdot \phi \cdot S_{h} \cdot FR}{B_{oi}}"
            )
            st.write(
                r"""
                $N_{f}$ - Reservas volumétricas de petróleo recuperáveis em barris de tanque de estoque (STB)  
                $7758$ - Barris por acre-pé  
                $A$ - Área de drenagem em acres  
                $h$ - Espessura do reservatório em pés  
                $\phi$ - Porosidade (fração decimal)  
                $S_{h}$ - Saturação de hidrocarbonetos (1-Sw) (fração decimal)  
                $FR$ - Fator de recuperação  
                $B_{oi}$ - Fator de volume do óleo, ou barris de reservatório por barril de tanque de estoque  

                """
            )
            cols = st.columns(3)
            with cols[0]:
                oil_acre = st.number_input("A (Acres)", min_value=0.00)
                oil_phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="oil_reserve_phi",
                )

            with cols[1]:
                oil_h = st.number_input("h (ft)", min_value=0.00)
                oil_fr = st.number_input("FR (Decimal)", min_value=0.00, max_value=1.00)

            with cols[2]:
                oil_sh = st.number_input(
                    r"$S_{h}$ (decimal)", min_value=0.00, max_value=1.00
                )
                oil_boi = st.number_input(r"$B_{oi}$ (Bbls/STB)", min_value=0.01)

            if st.button("Calcular Reservas"):
                try:
                    oil_nf = (
                        7758 * oil_acre * oil_h * oil_phi * oil_sh * oil_fr
                    ) / oil_boi
                    st.metric("Reservas de Óleo/Petróleo", value=f"{oil_nf:.2f} STB")
                except Exception as e:
                    st.warning(f"Ocorreu um erro: {e}")

        with reserve_tabs[1]:
            st.latex(r"B_{oi} = 1.05 + 0.5 \cdot (\frac{GOR}{100})")
            st.write(
                r"""
                $B_{oi}$ - Fator de volume do óleo, ou barris de reservatório por barril em tanque de superfície  
                $GOR$ - Razão Óleo-Gás
                """
            )
            cols = st.columns(3)
            with cols[1]:
                oil_GOR = st.number_input("GOR (SCF/STB)", min_value=0.00)

            if st.button("Calcular", key="boi"):
                boi_result = 1.05 + 0.5 * (oil_GOR / 100)
                st.metric(
                    "Fator de Volume do Óleo ", value=f"{boi_result:.4f} Bbls/STB"
                )

        with reserve_tabs[2]:
            st.latex(r"GOR = \frac{Gas_{cubic feet}}{Oil_{barrels}}")

            cols = st.columns(2)
            with cols[0]:
                gor_gas = st.number_input("Gás (pés cúbicos)", min_value=0.00)
            with cols[1]:
                gor_oil = st.number_input("Óleo (Bbls)", min_value=0.00)

            if st.button("Calcular", key="gor"):
                gor_final = gor_gas / gor_oil
                st.metric("Razão Óleo-Gás", value=f"{gor_final} SFC/STB")

    with st.expander("Gás"):
        list_of_gas_reserves_tab = [
            "Reservas de Gás",
            "Reservas de Gás - Cálculo Alternativo",
        ]
        gas_reserve_tabs = st.tabs(list_of_gas_reserves_tab)

        with gas_reserve_tabs[0]:
            st.latex(
                r"G_{f} = 43560 \cdot A \cdot h \cdot \phi \cdot S_{h} \cdot B_{gi} \cdot FR"
            )

            st.write(
                r"""
                Onde:  
                $G_{f}$ - Reservas volumétricas recuperáveis de gás em pés cúbicos padrão (SCF)  
                $43560$ - Área de 1 acre, em pés quadrados  
                $A$ - Área de drenagem, em acres  
                $h$ - Espessura do reservatório, em pés  
                $\phi$ - Porosidade, fração decimal  
                $S_{h}$ - Saturação de hidrocarbonetos $(1 - Sw)$, fração decimal  
                $RF$ - Fator de recuperação  
                $B_{gi}$ - Fator de volume do gás (em SCF/pé cúbico)
                """
            )

            gas_f_tabs = st.tabs(["Cálculo da Reserva", r"Fator de Volume do Gás ($B_{gi}$)"])
            
            with gas_f_tabs[0]:

                cols = st.columns(3)
                with cols[0]:
                    gas_acre = st.number_input("A (Acres)", min_value=0.00, key="gas_acre")
                    gas_phi = st.number_input(
                        r"$\phi$ (decimal)",
                        min_value=0.00,
                        max_value=1.00,
                        key="gas_phi",
                    )

                with cols[1]:
                    gas_h = st.number_input("h (ft)", min_value=0.00, key="gas_h")
                    gas_fr = st.number_input(
                        "FR (decimal)", min_value=0.00, max_value=1.00, key="gas_fr"
                    )

                with cols[2]:
                    gas_sh = st.number_input(
                        r"$S_{h}$ (decimal)",
                        min_value=0.00,
                        max_value=1.00,
                        key="gas_sh",
                    )
                    gas_boi = st.number_input(
                        r"$B_{gi}$ (Bbls/STB)",
                        min_value=0.01,
                        key="gas_boi",
                    )

                if st.button("Calcular Reservas", key="gas"):
                    try:
                        gas_nf = (
                            43560 * gas_acre * gas_h * gas_phi * gas_sh * gas_fr * gas_boi
                        )
                        st.metric("Reservas de Gás", value=f"{gas_nf:.2f} Stock-Tank Barrel")
                    except Exception as e:
                        st.warning(f"Ocorreu um erro: {e}")
                        
            with gas_f_tabs[1]:
                cols = st.columns(3)
                with cols[0]:
                    formation_temp = st.number_input("Temp. do Reservatório (ºF)", min_value=0.00)
                with cols[1]:
                    reservoir_pressure = st.number_input("Pressão do Reservatório (psi)", min_value=0.01)
                with cols[2]:
                    compressibility_factor = st.number_input("Fator de Compressibilidade do Gás", min_value=0.00)
                    
                if st.button("Calcular", key="bgf"):
                    bgf = (0.02827 * compressibility_factor * (459.7 + formation_temp)) / reservoir_pressure
                    st.metric(r"Gas Volume Factor ($B_{gi}$)", value=f"{bgf:.2f} SCF/CF")

        with gas_reserve_tabs[1]:
            st.latex(
                r"G_{f} = 43560 \cdot A \cdot h \cdot \phi \cdot S_{h} \cdot \left(\frac{P_{f2}}{P_{f1}}\right) \cdot FR"
            )

            st.write(
                r"""
                Onde:  
                $P_{f1}$ - Pressão da Superfície (psi)  - aproximadamente 15 psi  
                $P_{f2}$ - Pressão do Reservatório (psi)
                """
            )
            press_depth_opts = st.radio("Escolha uma opção de input", options=["Profundidade", "Pressão"], horizontal=True)
            cols = st.columns(3)
            with cols[0]:
                gas_acre = st.number_input("A (Acres)", min_value=0.00, key="gas_acre_alternative")
                gas_phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="gas_phi_alternative",
                )

            with cols[1]:
                gas_h = st.number_input("h (ft)", min_value=0.00, key="gas_h_alternative")
                gas_fr = st.number_input(
                    "FR (decimal)", min_value=0.00, max_value=1.00, key="gas_fr_alternative"
                )

            with cols[2]:
                gas_sh = st.number_input(
                    r"$S_{h}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="gas_sh_alternative",
                )
                if press_depth_opts == "Pressão":
                    pf2_pf1 = st.number_input(
                        r"Razão Pf2/Pf1 (SCF/cubic ft)",
                        min_value=0.01,
                        key="pf2_pf1",
                    )
                if press_depth_opts == "Profundidade":
                    depth_ft = st.number_input(
                        r"Profundidade (ft)",
                        min_value=0.01,
                        key="depth_ft",
                    )
                    pf2_pf1 = (0.43 * depth_ft) / 15

            if st.button("Calcular Reservas", key="gas_alternative"):
                try:
                    gas_nf = (
                        43560 * gas_acre * gas_h * gas_phi * gas_sh * gas_fr * pf2_pf1
                    )
                    st.metric("Reservas de Gás", value=f"{gas_nf:.2f} Stock-Tank Barrel")
                except Exception as e:
                    st.warning(f"Ocorreu um erro: {e}")

            
