import streamlit as st


def render_oil_reserves():
    st.write(
        """
    The calculation of porosity and water saturation plays a crucial role when estimating
    oil and gas reserves, as a significant error in calculating these two values can lead to
    serious economic problems, especially when dealing with a giant reservoir.

    The recovery factor is another important parameter in reserve estimation calculations, and this
    value will depend on the natural drainage mechanism(s) of the reservoir (gas cap, aquifer, etc.),
    which are very different from each other. Additionally, the recovery factor can increase with the
    application of secondary and tertiary recovery techniques in the reservoir, but this improvement
    adds more costs to the exploration budget.  
    """
    )
    with st.expander("Oil"):
        list_of_reserves_tabs = [
            "Oil Reserves",
            r"Oil Volume Factor ($B_{oi}$)",
            "Gas-Oil Ratio (GOR)",
        ]

        reserve_tabs = st.tabs(list_of_reserves_tabs)

        with reserve_tabs[0]:
            st.latex(
                r"N_{f} = \frac{7758 \cdot A \cdot h \cdot \phi \cdot S_{h} \cdot RF}{B_{oi}}"
            )
            st.write(
                r"""
                $N_{f}$ - Volumetric recoverable oil reserves in stock-tank barrels (STB)  
                $7758$ - Barrels per acre-foot  
                $A$ - Drainage area in acres  
                $h$ - Reservoir thickness in feet  
                $\phi$ - Porosity (decimal)  
                $S_{h}$ - Hydrocarbon saturation $(1 - S_w)$ (decimal)  
                $RF$ - Recovery Factor  
                $B_{oi}$ - Oil volume factor, or reservoir barrels per stock-tank barrel  

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
                oil_fr = st.number_input("RF (Decimal)", min_value=0.00, max_value=1.00)

            with cols[2]:
                oil_sh = st.number_input(
                    r"$S_{h}$ (decimal)", min_value=0.00, max_value=1.00
                )
                oil_boi = st.number_input(r"$B_{oi}$ (Bbls/STB)", min_value=0.01)

            if st.button("Calculate Reserves"):
                try:
                    oil_nf = (
                        7758 * oil_acre * oil_h * oil_phi * oil_sh * oil_fr
                    ) / oil_boi
                    st.metric("Oil Reserves", value=f"{oil_nf:.2f} STB")
                except Exception as e:
                    st.warning(f"An error occurred: {e}")

        with reserve_tabs[1]:
            st.latex(r"B_{oi} = 1.05 + 0.5 \cdot (\frac{GOR}{100})")
            st.write(
                r"""
                $B_{oi}$ - Oil volume factor, or reservoir barrels per stock-tank barrel  
                $GOR$ - Gas-Oil Ratio
                """
            )
            cols = st.columns(3)
            with cols[1]:
                oil_GOR = st.number_input("GOR (SCF/STB)", min_value=0.00)

            if st.button("Calculate", key="boi"):
                boi_result = 1.05 + 0.5 * (oil_GOR / 100)
                st.metric("Oil Volume Factor ", value=f"{boi_result:.4f} Bbls/STB")

        with reserve_tabs[2]:
            st.latex(r"GOR = \frac{Gas_{cubic feet}}{Oil_{barrels}}")

            cols = st.columns(2)
            with cols[0]:
                gor_gas = st.number_input("Gás (cubic ft)", min_value=0.00)
            with cols[1]:
                gor_oil = st.number_input("Oil (Bbls)", min_value=0.00)

            if st.button("Calculate", key="gor"):
                gor_final = gor_gas / gor_oil
                st.metric("Gas-Oil Ratio", value=f"{gor_final} SFC/STB")

    with st.expander("Gas"):
        list_of_gas_reserves_tab = [
            "Gas Reserves",
            "Gas Reserves - Alternate",
        ]
        gas_reserve_tabs = st.tabs(list_of_gas_reserves_tab)

        with gas_reserve_tabs[0]:
            st.latex(
                r"G_{f} = 43560 \cdot A \cdot h \cdot \phi \cdot S_{h} \cdot B_{gi} \cdot RF"
            )

            st.write(
                r"""
                Onde:  
                $G_{f}$ - Volumetric recoverable gas reserves in standard cubic feet (SCF)  
                $43560$ - Area of 1 acre, in square feet  
                $A$ - Drainage area in acres  
                $h$ - Reservoir thickness in feet  
                $\phi$ - Porosity (decimal)  
                $S_{h}$ - Hydrocarbon Saturation $(1 - S_w)$ (decimal)  
                $RF$ - Recovery factor  
                $B_{gi}$ - Gas volume factor (in SCF/cubic ft)
                """
            )

            gas_f_tabs = st.tabs(
                ["Reserve Calculation", r"Gas Volume Factor ($B_{gi}$)"]
            )

            with gas_f_tabs[0]:

                cols = st.columns(3)
                with cols[0]:
                    gas_acre = st.number_input(
                        "A (Acres)", min_value=0.00, key="gas_acre"
                    )
                    gas_phi = st.number_input(
                        r"$\phi$ (decimal)",
                        min_value=0.00,
                        max_value=1.00,
                        key="gas_phi",
                    )

                with cols[1]:
                    gas_h = st.number_input("h (ft)", min_value=0.00, key="gas_h")
                    gas_fr = st.number_input(
                        "RF (decimal)", min_value=0.00, max_value=1.00, key="gas_fr"
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

                if st.button("Calculate Reservas", key="gas"):
                    try:
                        gas_nf = (
                            43560
                            * gas_acre
                            * gas_h
                            * gas_phi
                            * gas_sh
                            * gas_fr
                            * gas_boi
                        )
                        st.metric(
                            "Gas Reserves", value=f"{gas_nf:.2f} Stock-Tank Barrel"
                        )
                    except Exception as e:
                        st.warning(f"An error occurred: {e}")

            with gas_f_tabs[1]:
                cols = st.columns(3)
                with cols[0]:
                    formation_temp = st.number_input("$T_{f}$ (ºF)", min_value=0.00)
                with cols[1]:
                    reservoir_pressure = st.number_input("$P$ (psi)", min_value=0.01)
                with cols[2]:
                    compressibility_factor = st.number_input("$Z$", min_value=0.00)

                if st.button("Calculate", key="bgf"):
                    bgf = (
                        0.02827 * compressibility_factor * (459.7 + formation_temp)
                    ) / reservoir_pressure
                    st.metric(
                        r"Gas Volume Factor ($B_{gi}$)", value=f"{bgf:.2f} SCF/CF"
                    )

        with gas_reserve_tabs[1]:
            st.latex(
                r"G_{f} = 43560 \cdot A \cdot h \cdot \phi \cdot S_{h} \cdot \left(\frac{P_{f2}}{P_{f1}}\right) \cdot FR"
            )

            st.write(
                r"""
                Onde:  
                $P_{f1}$ - Surface pressure (psi)  - approximately 15 psi  
                $P_{f2}$ - Reservoir pressure (psi)
                """
            )
            press_depth_opts = st.radio(
                "Escolha uma opção de input",
                options=["Depth", "Pressure"],
                horizontal=True,
            )
            cols = st.columns(3)
            with cols[0]:
                gas_acre = st.number_input(
                    "A (Acres)", min_value=0.00, key="gas_acre_alternative"
                )
                gas_phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="gas_phi_alternative",
                )

            with cols[1]:
                gas_h = st.number_input(
                    "h (ft)", min_value=0.00, key="gas_h_alternative"
                )
                gas_fr = st.number_input(
                    "FR (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="gas_fr_alternative",
                )

            with cols[2]:
                gas_sh = st.number_input(
                    r"$S_{h}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="gas_sh_alternative",
                )
                if press_depth_opts == "Pressure":
                    pf2_pf1 = st.number_input(
                        r"$P_{f2}/P_{f1}$ (SCF/cubic ft)",
                        min_value=0.01,
                        key="pf2_pf1",
                    )
                if press_depth_opts == "Depth":
                    depth_ft = st.number_input(
                        r"Depth (ft)",
                        min_value=0.01,
                        key="depth_ft",
                    )
                    pf2_pf1 = (0.43 * depth_ft) / 15

            if st.button("Calculate Reserves", key="gas_alternative"):
                try:
                    gas_nf = (
                        43560 * gas_acre * gas_h * gas_phi * gas_sh * gas_fr * pf2_pf1
                    )
                    st.metric("Gas Reserves", value=f"{gas_nf:.2f} Stock-Tank Barrel")
                except Exception as e:
                    st.warning(f"An error occurred: {e}")
