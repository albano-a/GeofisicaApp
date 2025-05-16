import streamlit as st
import scripts.petrophysics.porosity as porosity
import scripts.petrophysics.shale_volume as sv

# TODO - Turn this into a class (future refactoring)


def render_porosity():
    st.write(
        r"""
        Porosity is an important petrophysical parameter of the rock, defined as the ratio between the pore volume of the rock and the total volume of the rock."""
    )
    st.latex(r"\text{Porosity} = \frac{\text{Pore Volume}}{\text{Total Volume}}")
    st.write(
        """
        This physical property limits the rock's ability to accumulate hydrocarbons (oil, condensates, or gas). However, porosity must be interconnected to add commercial value to a reservoir. There are total porosity and effective porosity, where the former relates to all the pores in a rock, and the latter only to the interconnected pores, which are more important during hydrocarbon production.
        Additionally, the shale volume affects the quality of reservoirs, which is why corrections must be made when calculating porosity, known as shale-corrected values.
        """
    )

    with st.expander("Density Log"):
        tab1, tab2 = st.tabs(["Density", "Density-Neutron"])
        with tab1:

            st.write(
                """
                    For the calculation of porosity derived from density logs, the equation considers the values of matrix density and fluid density (previously known in the literature), as well as the formation density of the study area. The expression is as follows:
                    """
            )
            st.latex(
                r"""
                    \phi_{D} = \frac{\rho_{ma} - \rho_{b}}{\rho_{ma} - \rho_{fl}}
                    """
            )
            st.write(
                r"""
            Where:
            
            - $\phi_{D}$ - Density log porosity  
            - $\rho_{ma}$ - Matrix density  
            - $\rho_{b}$ - Bulk density log 
            - $\rho_{fl}$ - Fluid density  
            """
            )
            rho_log = st.number_input(r"$\rho_{b}$ (g/cm³)", min_value=0.00)
            cols = st.columns(2)
            with cols[0]:
                rho_matrix = st.number_input(
                    r"$\rho_{ma}$ (g/cm³)",
                    value=2.65,
                    help="Sandstone: 2.65 g/cm3\n\nCarbonate: 2.71 g/cm3\n\nDolomite: 2.87 g/cm3",
                )
            with cols[1]:
                rho_fluid = st.number_input(
                    r"$\rho_{fl}$ (g/cm³)",
                    value=1.0,
                    help="SWBM: 1.00 g/cm3\n\nOBM: 0.85 g/cm3",
                )

            if st.button("Calculate", key=1):
                try:
                    result = porosity.density_porosity(rho_log, rho_matrix, rho_fluid)
                    if 0 < result < 1:
                        st.metric(
                            label="Porosity",
                            value=f"{result:.4f} | {result*100:.2f}%",
                        )
                    else:
                        st.error("The value must be between 0 and 1")
                except Exception as e:
                    st.warning(e)
        with tab2:
            st.write(
                """
            In gas-bearing formations, a combination is made between the values obtained from neutron and density logs. For those familiar with wells, it is known that when the curves of both logs intersect (crossover), we can infer the presence of a gas accumulation, although other parameters need to be considered, such as well conditions (caliper), among others. The expression is as follows:
            """
            )
            st.latex(
                r"""
            \phi_{NDgas} = \sqrt{\frac{\phi_{N}^2 + \phi_{D}^2}{2}} 
            """
            )
            st.write(
                r"""
            Where:
            
            $\phi_{NDgas}$ - Gas-bearing formations porosity  
            $\phi_{N}$ - Neutron log porosity  
            $\phi_{D}$ - Density log porosity  
            """
            )
            cols = st.columns(2)
            with cols[0]:
                phid = st.number_input(
                    r"$\phi_{D}$ (decimal)", min_value=0.00, max_value=1.00
                )
            with cols[1]:
                phin = st.number_input(r"$\phi_{N}$", min_value=0.00, max_value=1.00)
            squared_btn = st.radio("Squared?", options=["Sim", "Não"])

            if st.button("Calculate", key=2):
                try:
                    if squared_btn == "Sim":
                        result = porosity.neutron_density_porosity(
                            phid=phid, phin=phin, squared=True
                        )
                    elif squared_btn == "Não":
                        result = porosity.neutron_density_porosity(
                            phid=phid, phin=phin, squared=False
                        )
                    st.success(f"Porosity calculada: {result:.4f} | {result*100:.2f}%")
                except Exception as e:
                    st.warning(e)

    with st.expander("Sonic Log"):
        sonic_porosity_eqs = [
            "Wyllie *et al.*, 1958",
            "Raymer *et al.*, 1980",
            "Non-Consolidated Formations",
        ]
        sonic_tabs = st.tabs(sonic_porosity_eqs)
        with sonic_tabs[0]:
            st.write(
                """
            The calculation of porosity derived from the sonic log can be performed using the time-average equation by Wyllie (Wyllie *et al.*, 1958), expressed as follows:
            """
            )
            st.latex(
                r"\phi_{S} = \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}}"
            )
            st.write(
                r"""
                Where:  
                $\phi_{S}$ - Sonic porosity  
                $\Delta t_{ma}$ - Transit time of the matrix interval  
                $\Delta t_{log}$ - Transit time of the formation interval (obtained from the sonic log)  
                $\Delta t_{fl}$ - Transit time of the fluid interval
                """
            )
            cols = st.columns(3)
            with cols[0]:
                delta_t_log = st.number_input(
                    r"$\Delta t_{log}$",
                    min_value=0.0,
                )
            with cols[1]:
                delta_t_ma = st.number_input(
                    r"$\Delta t_{ma}$",
                    min_value=0.0,
                    value=55.5,
                    help="""
                    Sandstone: 55.5 us/ft\n\n
                    Limestone: 47.6 us/ft\n\n
                    Dolomite: 43.5 us/ft
                    """,
                )
            with cols[2]:
                delta_t_fl = st.number_input(
                    r"$\Delta t_{fl}$",
                    min_value=0.0,
                    value=189.0,
                    help="""
                    Water (SWBM): 189 us/ft\n\n
                    Oil (OBM): 205 us/ft
                    """,
                )
            if st.button("Calculate", key="sonic_porosity"):
                try:
                    result = porosity.sonic_porosity(
                        delta_t_log, delta_t_ma, delta_t_fl
                    )
                    if 0 < result < 1:
                        st.metric("Porosity", value=f"{result:.4g} | {result*100:.2f}%")
                    else:
                        st.error("The value must be between 0 and 1")
                except Exception as e:
                    st.warning(e)

        with sonic_tabs[1]:
            st.write(
                """
                Another way to calculate porosity derived from the sonic log is through the Raymer-Hunt-Gardner (RHG) equation (Raymer et al., 1980), which uses the matrix and sonic values, and is expressed as follows:
                """
            )
            st.latex(
                r"\phi_{S} = \frac{5}{8} \cdot \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{log}}"
            )
            st.write(
                r"""
                Where:  
                $\phi_{S}$ - sonic-derived porosity  
                $\Delta t_{ma}$ - transit time of the matrix interval  
                $\Delta t_{log}$ - transit time of the formation interval  
                """
            )
            cols = st.columns(2)
            with cols[0]:
                delta_t_log = st.number_input(
                    r"$\Delta t_{log}$",
                    min_value=0.0,
                    key="delta_t_log_raymer",
                )
                oil_correction = st.radio(
                    "Correct for Hydrocarbons?",
                    options=["No", "Gas", "Oil"],
                    horizontal=True,
                    help="Hydrocarbons distort sonic porosity, requiring correction.",
                )
            with cols[1]:
                delta_t_ma = st.number_input(
                    r"$\Delta t_{ma}$",
                    min_value=0.0,
                    value=55.5,
                    help="""
                    Sandstone: 55.5 us/ft\n\n
                    Limestone: 47.6 us/ft\n\n
                    Dolomite: 43.5 us/ft
                    """,
                    key="delta_t_ma_raymer",
                )
            if st.button("Calculate", key="raymer_porosity"):
                try:
                    phi = (5 / 8) * ((delta_t_log - delta_t_ma) / delta_t_log)
                    if oil_correction == "Oil":
                        phi *= 0.7
                        st.metric("Porosity", value=f"{phi:.4g} | {phi*100:.2f}%")
                    elif oil_correction == "Gas":
                        phi *= 0.9
                        st.metric("Porosity", value=f"{phi:.4g} | {phi*100:.2f}%")
                    else:
                        st.metric("Porosity", value=f"{phi:.4g} | {phi*100:.2f}%")
                except ZeroDivisionError as ze:
                    st.warning("Zero division error")

        with sonic_tabs[2]:
            unc_form_tabs = st.tabs(["Unconsolidated Formations", r"Compaction Factor"])

            with unc_form_tabs[0]:
                st.write(
                    """
                    To calculate sonic porosity in unconsolidated formations, we can start by multiplying the sonic porosity equation of Wyllie et al. (1958) by the inverse of a compaction factor. The equation is as follows:
                    """
                )
                st.latex(
                    r"\phi_{S} = \left( \frac{ \Delta t_{log} - \Delta t_{ma} }{ \Delta t_{fl} - \Delta t_{ma} } \right) \cdot \frac{1}{C_{p}}"
                )
                st.write(
                    r"""
                    Where:  
                    $\phi_{S}$ - Sonic porosity  
                    $C_{p}$ - Compaction factor  
                    $\Delta t_{ma}$ - Transit time of the matrix interval  
                    $\Delta t_{log}$ - Transit time of the formation interval (obtained from the sonic log)  
                    $\Delta t_{fl}$ - Transit time of the fluid interval 
                    """
                )
                cols = st.columns(2)
                with cols[0]:
                    delta_t_log = st.number_input(
                        r"$\Delta t_{log}$",
                        min_value=0.0,
                        key="unconsolidated_formation_log",
                    )
                    delta_t_fl = st.number_input(
                        r"$\Delta t_{fl}$",
                        min_value=0.0,
                        value=189.0,
                        help="""
                        Water (SWBM): 189 us/ft\n\n
                        Oil (OBM): 205 us/ft
                        """,
                        key="unconsolidated_formation_fl",
                    )

                with cols[1]:
                    compact_factor = st.number_input(
                        r"$C_{p}$",
                        min_value=0.0,
                    )

                    delta_t_ma = st.number_input(
                        r"$\Delta t_{ma}$",
                        min_value=0.0,
                        value=55.5,
                        help="""
                        Sandstone: 55.5 us/ft\n\n
                        Limestone: 47.6 us/ft\n\n
                        Dolomite: 43.5 us/ft
                        """,
                        key="unconsolidated_formation_ma",
                    )

                if st.button("Calculate", key="unconsolidated"):
                    phi_sonic = (
                        (delta_t_log - delta_t_ma) / (delta_t_fl - delta_t_ma)
                    ) * (1 / compact_factor)
                    st.metric(
                        label="Porosity",
                        value=f"{phi_sonic:.4g} | {phi_sonic*100:.2f}%",
                    )

            with unc_form_tabs[1]:
                st.write(
                    """
                    The compaction factor is calculated using the following equation, which takes into account the sonic porosity of a shale adjacent to the formation of interest:
                    """
                )
                st.latex(r"d = \frac{\Delta t_{sh} \cdot C}{100}")
                st.write(
                    r"""
                    Where:  
                    $\Delta t_{sh}$ - Transit time interval in a shale adjacent to the formation of interest  
                    $C$ - Constant, usually equal to 1.0 (Hilchie, 1978)  
                    """
                )
                cols = st.columns(2)
                with cols[0]:
                    dt_sh = st.number_input(
                        r"$\Delta t_{sh}$",
                        min_value=0.0,
                        placeholder="(us/ft)",
                    )
                with cols[1]:
                    constant = st.number_input("C", min_value=0.0, value=1.0)

                if st.button("Calculate", key="compact_form"):
                    result = (dt_sh * constant) / 100
                    st.metric(label="Fator de Compactação", value=f"{result:.4f}")

    with st.expander("Resistivity Log"):
        list_of_resistivity_tabs = [
            "Porosity",
            "Flushed Zone Porosity",
        ]

        resistivity_tabs = st.tabs(list_of_resistivity_tabs)

        with resistivity_tabs[0]:
            st.write(
                """
                Starting from the well-known Archie Equation, most famous for water resistivity calculations, 
                it is also used for determining porosity from resistivity. 
                This equation involves the values of the tortuosity factor, formation and water resistivities, 
                water saturation, and the cementation and saturation exponents, and is expressed as follows:
                """
            )
            st.latex(
                r"\phi = \left( \frac{ a \cdot R_{w} }{ R_{t} \cdot S_{w}^{n} } \right)^{\frac{1}{m}}"
            )
            st.write(
                r"""
                Where:
                $\phi$ - Porosity  
                $S_{w}$ - Water saturation in the uninvaded zone  
                $R_{w}$ - Formation water resistivity at formation temperature  
                $R_{t}$ - True formation resistivity (e.g., deep induction reading or deep laterolog corrected for invasion)  
                $a$ - Tortuosity factor  
                $m$ - Cementation exponent  
                $n$ - Saturation exponent  
                """
            )
            # first col - a, rt, n
            # second col - rw, sw, m
            cols = st.columns(2)
            with cols[0]:
                true_resistivity = st.number_input(
                    r"$R_{t}$ (ohm-m)",
                    min_value=0.0,
                )
                water_sat = st.number_input(
                    r"$S_{w}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="water_sat_1",
                )
                sat_exp = st.number_input(
                    r"$n$",
                    min_value=0.0,
                    help="Expoente de Saturação",
                    key="sat_exp_archie",
                )
            with cols[1]:
                res_water_form = st.number_input(
                    r"$R_{w}$ (ohm-m)",
                    min_value=0.0,
                )
                tort_factor = st.number_input(
                    r"$a$",
                    min_value=0.00,
                    help="Fator de Tortuosidade",
                    key="tort_factor_archie",
                )
                cement_exp = st.number_input(
                    r"$m$",
                    min_value=0.0,
                    help="Expoente de Cimentação",
                    key="cement_exp_1",
                )

            if st.button("Calculate", key="resistivity_derived_porosity"):
                try:
                    phi = (
                        (tort_factor * res_water_form)
                        / (true_resistivity * (water_sat) ** (sat_exp))
                    ) ** (1 / cement_exp)
                    if 0 < phi < 1:
                        st.metric(
                            "Resistivity Porosity",
                            value=f"{phi:.4g} | {phi*100:.2f}%",
                        )
                    else:
                        st.error("The value must be between 0 and 1")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        with resistivity_tabs[1]:
            st.write(
                """
                For the calculation of porosity derived from resistivity in the flushed zone,
                there are cases where it is necessary to apply a correction for residual hydrocarbons.
                In this situation, it is necessary to know the water saturation of the uninvaded zone and the value
                of the saturation exponent. The expression is summarized as follows:
                """
            )
            st.latex(
                r"\phi = \left( \frac{a \cdot R_{mf}}{S_{w}^{n} \cdot R_{xo}} \right)^{\frac{1}{m}}"
            )
            st.write(
                r"""
                Where:  
                $\phi$ - Porosity  
                $a$ - Tortuosity factor  
                $S_w$ - Water saturation of the uninvaded zone  
                $m$ - Cementation exponent  
                $n$ - Saturation exponent  
                $R_{mf}$ - Mud filtrate resistivity at formation temperature  
                $R_{xo}$ - Shallow resistivity obtained with very shallow reading tools, such as laterolog-8,   
                micro-spherically focused log, or microlaterolog  
                """
            )
            cols = st.columns(2)
            with cols[0]:
                true_resistivity = st.number_input(
                    r"$R_{xo}$ (ohm-m)",
                    min_value=0.0,
                )
                water_sat = st.number_input(
                    r"$S_{w}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="water_sat_2",
                )
                sat_exp = st.number_input(
                    r"$n$",
                    min_value=0.0,
                    help="Saturation Exponent",
                    key="sat_exp_archie_2",
                )
            with cols[1]:
                res_mud_filt = st.number_input(
                    r"$R_{mf}$ (ohm-m)",
                    min_value=0.0,
                )
                tort_factor = st.number_input(
                    r"$a$",
                    min_value=0.00,
                    help="Tortuosity Factor",
                    key="tort_factor_archie_2",
                )
                cement_exp = st.number_input(
                    r"$m$",
                    min_value=0.0,
                    help="Cementation Exponent",
                    key="cement_exp_2",
                )

            if st.button("Calculate", key="resistivity_derived_porosity_flushed_zone"):
                try:
                    phi = (
                        (tort_factor * res_water_form)
                        / (true_resistivity * (water_sat) ** (sat_exp))
                    ) ** (1 / cement_exp)
                    if 0 < phi < 1:
                        st.metric(
                            "Resistivity Porosity - Flushed Zone",
                            value=f"{phi:.4g} | {phi*100:.2f}%",
                        )
                    else:
                        st.error("The value must be between 0 and 1")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with st.expander("Shale Correction"):
        # Abas: Dewan (densidade, sonico neutrao), Schlumberger (densidade, neutrao)
        list_of_tabs_shale_correction = ["Dewan", "Schlumberger"]

        shale_correction_tabs = st.tabs(list_of_tabs_shale_correction)

        with shale_correction_tabs[0]:
            st.write(
                """
                Dewan (1983) proposed a series of corrections for porosity values derived from density, sonic, and neutron logs, taking into account the Shale Volume and the corresponding porosity of a shale adjacent to the depth of interest. For each type of log, Dewan provided a specific equation to correct the porosity, considering the influence of Shale Volume and the porosity value in the nearby shale.
                """
            )
            st.latex(r"\phi_{cor} = \phi - V_{shale} \cdot \phi_{shale}")
            st.write(
                r"""
                Where:
                $\phi_{cor}$ - Porosity from Density, Sonic, or Neutron log - corrected for shale.
                $\phi$ - Porosity from Density, Sonic, or Neutron log
                $\phi_{shale}$ - Porosity from logs in a nearby shale
                $V_{shale}$ - Shale Volume 
                """
            )
            log_opts = st.radio(
                "Select the log:",
                options=["Density", "Sonic", "Neutron"],
                horizontal=True,
            )
            cols = st.columns(3)
            with cols[0]:
                phi = st.number_input(
                    r"$\phi$ (decimal)", min_value=0.00, max_value=1.00
                )
            with cols[1]:
                vshale = st.number_input(
                    r"$V_{Shale}$ (decimal)", min_value=0.00, max_value=1.00
                )
            with cols[2]:
                phi_shale = st.number_input(
                    r"$\phi_{shale}$ (decimal)", min_value=0.00, max_value=1.00
                )
            if st.button("Calculate", key="dewan"):
                try:
                    phi_cor = phi - vshale * phi_shale
                    if log_opts == "Density":
                        st.metric(
                            "Density log porosity corrected for Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                    elif log_opts == "Sonic":
                        st.metric(
                            "Sonic log porosity corrected for Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                    elif log_opts == "Neutron":
                        st.metric(
                            "Neutron log porosity corrected for Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                except Exception as e:
                    st.warning(f"An error occurred: {e}")

        with shale_correction_tabs[1]:
            st.write(
                """
                Schlumberger (1975) proposed corrections for porosity values derived from density and neutron logs. In both cases, the equations include the Shale Volume and the porosity value of a shale adjacent to the depth of interest. The expressions are as follows:
                """
            )
            cols = st.columns(2)
            with cols[0]:
                st.latex(
                    r"\phi_{De} = \phi_{D} - \left[(\frac{\phi_{Dshale}}{0.45}) \cdot 0.13 \cdot V_{shale} \right]"
                )
                st.write(
                    r"""
                    Where:  
                    $\phi_{De}$ - Density log porosity corrected for shale  
                    $\phi_{D}$ - Density log porosity  
                    $\phi_{DShale}$ - Density log porosity in an adjacent shale  
                    $V_{shale}$- Shale Volume  
                    """
                )
            with cols[1]:
                st.latex(
                    r"\phi_{Ne} = \phi_{N} - \left[(\frac{\phi_{Nshale}}{0.45}) \cdot 0.03 \cdot V_{shale} \right]"
                )
                st.write(
                    r"""
                    Where:  
                    $\phi_{Ne}$ - Neutron log porosity corrected for shale  
                    $\phi_{N}$ - Neutron log porosity  
                    $\phi_{NShale}$ - Neutron log porosity in an adjacent shale  
                    $V_{shale}$- Shale Volume  
                    """
                )
            opts_schlumberger = st.radio(
                "Choose a log:", options=["Density", "Neutron"], horizontal=True
            )
            cols = st.columns(3)
            with cols[0]:
                phi_dn = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="schlumberger_phi",
                )
            with cols[1]:
                phi_dnshale = st.number_input(
                    r"$\phi_{Shale}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="schlumberger_phi_dnshale",
                )
            with cols[2]:
                vshale = st.number_input(
                    r"$V_{shale}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="schlumberger_vshale",
                )

            if st.button(
                "Calculate (Density)"
                if opts_schlumberger == "Density"
                else "Calculate (Neutron)"
            ):
                try:
                    if opts_schlumberger == "Density":
                        phi_result = phi_dn - ((phi_dnshale / 0.45) * 0.13 * vshale)
                        label = "Corrected Porosity (Density)"
                    else:
                        phi_result = phi_dn - ((phi_dnshale / 0.45) * 0.03 * vshale)
                        label = "Corrected Porosity (Neutron)"
                    st.metric(
                        label,
                        f"{phi_result:.4g} | {phi_result*100:.2f}%",
                    )
                except Exception as e:
                    st.warning(f"An error occurred: {e}")
