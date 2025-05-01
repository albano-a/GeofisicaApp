import streamlit as st
import scripts.petrophysics.porosity as porosity
import scripts.petrophysics.shale_volume as sv

# TODO - Turn this into a class (future refactoring)


def render_porosity():
    st.subheader("Porosity")

    st.write(
        r"""
        Porosity is an important petrophysical parameter of the rock, defined as the ratio between the pore volume of the rock and the total volume of the rock."""
    )
    st.latex(r"\text{Porosity} = \frac{\text{Volume dos Poros}}{\text{Volume Total}}")
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
            "Formações Não-Consolidadas",
        ]
        sonic_tabs = st.tabs(sonic_porosity_eqs)
        with sonic_tabs[0]:
            st.write(
                """
            O cálculo da porosity derivada do perfil sônico pode ser feito utilizando a equação da média de tempos de Wyllie (Wyllie *et al.*, 1958), expressa da seguinte forma:
            """
            )
            st.latex(
                r"\phi_{S} = \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}}"
            )
            st.write(
                r"""
                Onde:  
                $\phi_{S}$ - Porosity sônica  
                $\Delta t_{ma}$ - Tempo de trânsito da matriz  
                $\Delta t_{log}$ - Tempo de trânsito da formação (obtido do perfil sônico)  
                $\Delta t_{fl}$ - Tempo de trânsito do fluido de perfuração
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
                    Arenito: 55.5 us/ft\n\n
                    Carbonato: 47.6 us/ft\n\n
                    Dolomita: 43.5 us/ft
                    """,
                )
            with cols[2]:
                delta_t_fl = st.number_input(
                    r"$\Delta t_{fl}$",
                    min_value=0.0,
                    value=189.0,
                    help="""
                    Água (SWBM): 189 us/ft\n\n
                    Óleo (OBM): 205 us/ft
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
                Outra forma de Calculate a porosity derivada do sônico é através da equação de Raymer-Hunt-Gardner (RHG) (Raymer et al., 1980), que a calcula utilizando os valores de matriz e de sônico, e é expressa da seguinte forma:
                """
            )
            st.latex(
                r"\phi_{S} = \frac{5}{8} \cdot \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{log}}"
            )
            st.write(
                r"""
                Onde:  
                $\phi_{S}$ - porosity derivada do sônico  
                $\Delta t_{ma}$ - tempo de trânsito do intervalo na matriz  
                $\Delta t_{log}$ - tempo de trânsito do intervalo na formação  
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
                    Para Calculate a porosity sônica em formações inconsolidadas, podemos começar multiplicando a equação de porosity sônica de Wyllie et al. (1958) pela expressão inversa de um fator de compactação. A equação é a seguinte:
                    """
                )
                st.latex(
                    r"\phi_{S} = \left( \frac{ \Delta t_{log} - \Delta t_{ma} }{ \Delta t_{fl} - \Delta t_{ma} } \right) \cdot \frac{1}{C_{p}}"
                )
                st.write(
                    r"""
                    Onde:  
                    $\phi_{S}$ - Porosity sônica  
                    $C_{p}$ - Fator de compactação  
                    $\Delta t_{ma}$ - Tempo de trânsito do intervalo na matriz  
                    $\Delta t_{log}$ - Tempo de trânsito do intervalo na formação (obtido do perfil sônico)  
                    $\Delta t_{fl}$ - Tempo de trânsito do intervalo no fluido 
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
                        Água (SWBM): 189 us/ft\n\n
                        Óleo (OBM): 205 us/ft
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
                        Arenito: 55.5 us/ft\n\n
                        Carbonato: 47.6 us/ft\n\n
                        Dolomita: 43.5 us/ft
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
                    O fator de compactação é calculado pela seguinte equação, que leva em consideração a porosity sônica de uma argila adjacente à formação de interesse:
                    """
                )
                st.latex(r"d = \frac{\Delta t_{sh} \cdot C}{100}")
                st.write(
                    r"""
                    Onde:  
                    $\Delta t_{sh}$ - Tempo de trânsito do intervalo em uma argila adjacente à formação de interesse  
                    $C$ - Constante, normalmente igual a 1,0 (Hilchie, 1978)  
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
            "Porosity de Zona Invadida",
        ]

        resistivity_tabs = st.tabs(list_of_resistivity_tabs)

        with resistivity_tabs[0]:
            st.write(
                """
                Partindo da conhecida Equação de Archie, mais famosa pelos cálculos de resistividade da água, 
                ela também é utilizada para a determinação da porosity a partir da resistividade. 
                Esta equação envolve os valores do fator de tortuosidade, resistividades da formação e da 
                água, saturação de água, e os expoentes de saturação e de cimentação, sendo expressa da seguinte forma:
                """
            )
            st.latex(
                r"\phi = \left( \frac{ a \cdot R_{w} }{ R_{t} \cdot S_{w}^{n} } \right)^{\frac{1}{m}}"
            )
            st.write(
                r"""
                Onde:
                $\phi$ - Porosity  
                $S_{w}$ - saturação de água da zona não invadida  
                $R_{w}$ - Resistividade da água da formação na temperatura de formação  
                $R_{t}$ - Resistividade verdadeira da formação (por exemplo, leitura profunda da indução ou laterolog profunda corrigida para invasão)  
                $a$ - Fator de tortuosidade  
                $m$ - Expoente de cimentação  
                $n$ - Expoente de saturação  
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
                            "Porosity pela Resistividade",
                            value=f"{phi:.4g} | {phi*100:.2f}%",
                        )
                    else:
                        st.error("O valor de porosity deve ser entre 0 e 1")
                except Exception as e:
                    st.error(f"Um erro ocorreu: {e}")

        with resistivity_tabs[1]:
            st.write(
                """
                Para o cálculo da porosity derivada da resistividade na zona invadida, 
                existem casos em que é necessário aplicar uma correção para hidrocarbonetos residuais. 
                Nessa situação, é preciso conhecer a saturação de água da zona não invadida e o valor 
                do expoente de saturação. A expressão é resumida da seguinte forma:
                """
            )
            st.latex(
                r"\phi = \left( \frac{a \cdot R_{mf}}{S_{w}^{n} \cdot R_{xo}} \right)^{\frac{1}{m}}"
            )
            st.write(
                r"""
                Onde:  
                $\phi$ - Porosity  
                $a$ - Fator de tortuosidade  
                $S_w$ - Saturação de água da zona não invadida  
                $m$ - Expoente de cimentação  
                $n$ - Expoente de saturação  
                $R_{mf}$ - Resistividade do filtrado de lama na temperatura de formação  
                $R_{xo}$ - Resistividade rasa obtida com ferramentas de leitura muito superficial, como o laterolog-8,   
                o perfil microesfericamente focado ou o microlaterolog  
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
                    help="Expoente de Saturação",
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
                    help="Fator de Tortuosidade",
                    key="tort_factor_archie_2",
                )
                cement_exp = st.number_input(
                    r"$m$",
                    min_value=0.0,
                    help="Expoente de Cimentação",
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
                            "Porosity pela Resistividade - Zona Invadida",
                            value=f"{phi:.4g} | {phi*100:.2f}%",
                        )
                    else:
                        st.error("O valor de porosity deve ser entre 0 e 1")
                except Exception as e:
                    st.error(f"Um erro ocorreu: {e}")

    with st.expander("Shale Correction"):
        # Abas: Dewan (densidade, sonico neutrao), Schlumberger (densidade, neutrao)
        list_of_tabs_shale_correction = ["Dewan", "Schlumberger"]

        shale_correction_tabs = st.tabs(list_of_tabs_shale_correction)

        with shale_correction_tabs[0]:
            st.write(
                """
                Dewan (1983) propôs uma série de correções para valores de porosity derivados de logs de densidade, 
                sônico e de nêutrons, levando em consideração o Shale Volume e a porosity correspondente de uma 
                argila adjacente à profundidade de interesse. Para cada tipo de log, Dewan forneceu uma equação específica
                para corrigir a porosity, considerando a influência do Shale Volume e o valor da porosity na argila próxima.
                """
            )
            st.latex(r"\phi_{cor} = \phi - V_{shale} \cdot \phi_{shale}")
            st.write(
                r"""
                Onde:
                $\phi_{cor}$ - Porosity pelo perfil de Densidade, Sônico ou Neutrão - corrigido para shale.
                $\phi$ - Porosity pelo perfil de Densidade, Sônico ou Neutrão
                $\phi_{shale}$ - Porosity pelos perfis em um shale próximo
                $V_{shale}$ - Shale Volume 
                """
            )
            log_opts = st.radio(
                "Selecione o perfil:",
                options=["Densidade", "Sônico", "Neutrão"],
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
                    if log_opts == "Densidade":
                        st.metric(
                            "Porosity pela Densidade corrigida para Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                    elif log_opts == "Sônico":
                        st.metric(
                            "Porosity pelo Sônico corrigida para Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                    elif log_opts == "Neutrão":
                        st.metric(
                            "Porosity pelo Neutrão corrigida para Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                except Exception as e:
                    st.warning(f"Um erro ocorreu: {e}")

        with shale_correction_tabs[1]:
            st.write(
                """
                Schlumberger (1975) propôs correções para os valores de porosity 
                derivados de logs de densidade e de neutrão. Em ambos os casos, as 
                equações incluem o Shale Volume e o valor de porosity de uma 
                argila próxima à profundidade de interesse. As expressões são as seguintes:
                """
            )
            cols = st.columns(2)
            with cols[0]:
                st.latex(
                    r"\phi_{De} = \phi_{D} - \left[(\frac{\phi_{Dshale}}{0.45}) \cdot 0.13 \cdot V_{shale} \right]"
                )
                st.write(
                    r"""
                    Onde:  
                    $\phi_{De}$ - porosity do log de densidade corrigida para shale  
                    $\phi_{D}$ - porosity do log de densidade  
                    $\phi_{DShale}$ - porosity do log de densidade em um shale adjacente  
                    $V_{shale}$- Shale Volume  
                    """
                )
            with cols[1]:
                st.latex(
                    r"\phi_{Ne} = \phi_{N} - \left[(\frac{\phi_{Nshale}}{0.45}) \cdot 0.03 \cdot V_{shale} \right]"
                )
                st.write(
                    r"""
                    Onde:  
                    $\phi_{Ne}$ - porosity do log de neutrão corrigida para shale  
                    $\phi_{N}$ - porosity do log de neutrão  
                    $\phi_{NShale}$ - porosity do log de neutrão em um shale adjacente  
                    $V_{shale}$- Shale Volume  
                    """
                )
            opts_schlumberger = st.radio(
                "Escolha um perfil:", options=["Densidade", "Neutrão"], horizontal=True
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
                "Calculate (Densidade)"
                if opts_schlumberger == "Densidade"
                else "Calculate (Neutrão)"
            ):
                try:
                    phi_result = phi_dn - (
                        (phi_dnshale / 0.45) * 0.03
                        if opts_schlumberger == "Neutrão"
                        else 0.13 * vshale
                    )
                    st.metric(
                        (
                            "Porosity corrigida (Densidade)"
                            if opts_schlumberger == "Densidade"
                            else "Porosity corrigida (Neutrão)"
                        ),
                        f"{phi_result:.4g} | {phi_result*100:.2f}%",
                    )
                except Exception as e:
                    st.warning(f"Um erro ocorreu: {e}")
