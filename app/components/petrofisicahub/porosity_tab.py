import streamlit as st
import scripts.petrophysics.porosity as porosity
import scripts.petrophysics.shale_volume as sv

# TODO - Turn this into a class (future refactoring)


def render_porosity():
    st.subheader("Porosidade")

    st.write(
        r"""
        Porosidade é um importante parâmetro petrofísico da rocha, que é definido como a relação entre o volume dos poros da rocha e o volume total da rocha.

        $\text{Porosidade} = \frac{\text{Volume dos Poros}}{\text{Volume Total}}$

        Essa propriedade física limita a rocha no momento de acumular hidrocarbonetos (óleo, condensados ou gás), porém, a porosidade deve estar interconectada para adicionar valor comercial a um reservatório. Existem porosidade total e porosidade efetiva, onde a primeira está relacionada a todos os poros de uma rocha, e a segunda, apenas aos poros interconectados, que são mais importantes no momento da produção de hidrocarbonetos.
        Além disso, o volume de folhelho afeta a qualidade dos reservatórios, e é por isso que correções têm que ser feitas ao calcular a porosidade, conhecidas como valores corrigidos para folhelho. 
        """
    )

    with st.expander("Porosidade - Perfil de Densidade"):
        tab1, tab2 = st.tabs(["Densidade", "Densidade-Neutrão"])
        with tab1:

            st.write(
                """
                    Para o cálculo da porosidade derivada dos registros de densidade, a equação leva em consideração os valores de densidade da matriz e do fluido (anteriormente conhecidos na literatura), e a densidade da formação da área de estudo. A expressão é a seguinte:
                    """
            )
            st.latex(
                r"""
                    \phi_{D} = \frac{\rho_{ma} - \rho_{b}}{\rho_{ma} - \rho_{fl}}
                    """
            )
            st.write(
                r"""
            Onde:
            
            - $\phi_{D}$ - Porosidade do log de densidade  
            - $\rho_{ma}$ - Densidade da matriz  
            - $\rho_{b}$ - Densidade da formação a granel  
            - $\rho_{fl}$ - Densidade do fluido  
            """
            )
            rho_log = st.number_input("Densidade Bulk do Perfil")
            cols = st.columns(2)
            with cols[0]:
                rho_matrix = st.number_input(
                    "Densidade da Matriz",
                    value=2.65,
                    help="Arenito: 2.65 g/cm3\n\nCarbonato: 2.71 g/cm3\n\nDolomita: 2.87 g/cm3",
                )
            with cols[1]:
                rho_fluid = st.number_input(
                    "Densidade do Fluido",
                    value=1.0,
                    help="Água: 1.00 g/cm3\n\nÓleo: 0.85 g/cm3",
                )

            if st.button("Calcular", key=1):
                try:
                    result = porosity.density_porosity(rho_log, rho_matrix, rho_fluid)
                    if 0 < result < 1:
                        st.metric(
                            label="Porosidade",
                            value=f"{result:.4f} | {result*100:.2f}%",
                        )
                    else:
                        st.error("Erro - O valor deve estar entre 0 e 1")
                except Exception as e:
                    st.warning(e)
        with tab2:
            st.write(
                """
            Em formações portadoras de gás, é feita uma combinação entre os valores obtidos dos perfis de neutrão e densidade. Para aqueles que sabem sobre poços, se sabe que quando as curvas de ambos os logs se cruzam (crossover), podemos inferir a presença de uma acumulação de gás, embora outros parâmetros precisem ser levados em consideração, como as condições do poço (caliper), entre outros. A expressão é a seguinte:
            """
            )
            st.latex(
                r"""
            \phi_{NDgas} = \sqrt{\frac{\phi_{N}^2 + \phi_{D}^2}{2}} 
            """
            )
            st.write(
                r"""
            Onde:
            
            $\phi_{NDgas}$ = porosidade das formações com gás  
            $\phi_{N}$ = porosidade do perfil neutrão  
            $\phi_{D}$ = porosidade do perfil de densidade  
            """
            )
            cols = st.columns(2)
            with cols[0]:
                phid = st.number_input(
                    "Porosidade efetiva a partir da Densidade (decimal)"
                )
            with cols[1]:
                phin = st.number_input("Porosidade efetiva pelo Neutrão (decimal)")
            squared_btn = st.radio("Ao quadrado?", options=["Sim", "Não"])

            if st.button("Calcular", key=2):
                try:
                    if squared_btn == "Sim":
                        result = porosity.neutron_density_porosity(
                            phid=phid, phin=phin, squared=True
                        )
                    elif squared_btn == "Não":
                        result = porosity.neutron_density_porosity(
                            phid=phid, phin=phin, squared=False
                        )
                    st.success(
                        f"Porosidade calculada: {result:.4f} | {result*100:.2f}%"
                    )
                except Exception as e:
                    st.warning(e)

    with st.expander("Porosidade - Perfil Sônico"):
        sonic_porosity_eqs = [
            "Wyllie *et al.*, 1958",
            "Raymer *et al.*, 1980",
            "Formações Não-Consolidadas",
        ]
        sonic_tabs = st.tabs(sonic_porosity_eqs)
        with sonic_tabs[0]:
            st.write(
                """
            O cálculo da porosidade derivada do perfil sônico pode ser feito utilizando a equação da média de tempos de Wyllie (Wyllie *et al.*, 1958), expressa da seguinte forma:
            """
            )
            st.latex(
                r"\phi_{S} = \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}}"
            )
            st.write(
                r"""
                Onde:  
                $\phi_{S}$ - Porosidade sônica  
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
            if st.button("Calcular", key="sonic_porosity"):
                try:
                    result = porosity.sonic_porosity(
                        delta_t_log, delta_t_ma, delta_t_fl
                    )
                    if 0 < result < 1:
                        st.metric(
                            "Porosidade", value=f"{result:.4g} | {result*100:.2f}%"
                        )
                    else:
                        st.error("A porosidade precisa estar entre 0 e 1")
                except Exception as e:
                    st.warning(e)

        with sonic_tabs[1]:
            st.write(
                """
                Outra forma de calcular a porosidade derivada do sônico é através da equação de Raymer-Hunt-Gardner (RHG) (Raymer et al., 1980), que a calcula utilizando os valores de matriz e de sônico, e é expressa da seguinte forma:
                """
            )
            st.latex(
                r"\phi_{S} = \frac{5}{8} \cdot \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{log}}"
            )
            st.write(
                r"""
                Onde:  
                $\phi_{S}$ - porosidade derivada do sônico  
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
                    "Corrigir para Hidrocarbonetos?",
                    options=["Não", "Gás", "Óleo"],
                    horizontal=True,
                    help="Hidrocarbonetos distorcem a porosidade sônica, exigindo correção.",
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
                    key="delta_t_ma_raymer",
                )
            if st.button("Calcular", key="raymer_porosity"):
                try:
                    phi = (5 / 8) * ((delta_t_log - delta_t_ma) / delta_t_log)
                    if oil_correction == "Óleo":
                        phi *= 0.7
                        st.metric("Porosidade", value=f"{phi:.4g} | {phi*100:.2f}%")
                    elif oil_correction == "Gás":
                        phi *= 0.9
                        st.metric("Porosidade", value=f"{phi:.4g} | {phi*100:.2f}%")
                    else:
                        st.metric("Porosidade", value=f"{phi:.4g} | {phi*100:.2f}%")
                except ZeroDivisionError as ze:
                    st.warning("Divisão por zero!")

        with sonic_tabs[2]:
            unc_form_tabs = st.tabs(
                ["Formações Não-Consolidadas", r"Fator de Compactação"]
            )

            with unc_form_tabs[0]:
                st.write(
                    """
                    Para calcular a porosidade sônica em formações inconsolidadas, podemos começar multiplicando a equação de porosidade sônica de Wyllie et al. (1958) pela expressão inversa de um fator de compactação. A equação é a seguinte:
                    """
                )
                st.latex(
                    r"\phi_{S} = \left( \frac{ \Delta t_{log} - \Delta t_{ma} }{ \Delta t_{fl} - \Delta t_{ma} } \right) \cdot \frac{1}{C_{p}}"
                )
                st.write(
                    r"""
                    Onde:  
                    $\phi_{S}$ - Porosidade sônica  
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

                if st.button("Calcular", key="unconsolidated"):
                    phi_sonic = (
                        (delta_t_log - delta_t_ma) / (delta_t_fl - delta_t_ma)
                    ) * (1 / compact_factor)
                    st.metric(
                        label="Porosidade",
                        value=f"{phi_sonic:.4g} | {phi_sonic*100:.2f}%",
                    )

            with unc_form_tabs[1]:
                st.write(
                    """
                    O fator de compactação é calculado pela seguinte equação, que leva em consideração a porosidade sônica de uma argila adjacente à formação de interesse:
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

                if st.button("Calcular", key="compact_form"):
                    result = (dt_sh * constant) / 100
                    st.metric(label="Fator de Compactação", value=f"{result:.4f}")

    with st.expander("Porosidade - Perfil Resistividade"):
        list_of_resistivity_tabs = [
            "Porosidade",
            "Porosidade de Zona Invadida",
        ]

        resistivity_tabs = st.tabs(list_of_resistivity_tabs)

        with resistivity_tabs[0]:
            st.write(
                """
                Partindo da conhecida Equação de Archie, mais famosa pelos cálculos de resistividade da água, 
                ela também é utilizada para a determinação da porosidade a partir da resistividade. 
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
                $\phi$ - Porosidade  
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
                            "Porosidade pela Resistividade",
                            value=f"{phi:.4g} | {phi*100:.2f}%",
                        )
                    else:
                        st.error("O valor de porosidade deve ser entre 0 e 1")
                except Exception as e:
                    st.error(f"Um erro ocorreu: {e}")

        with resistivity_tabs[1]:
            st.write(
                """
                Para o cálculo da porosidade derivada da resistividade na zona invadida, 
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
                $\phi$ - Porosidade  
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
                            "Porosidade pela Resistividade - Zona Invadida",
                            value=f"{phi:.4g} | {phi*100:.2f}%",
                        )
                    else:
                        st.error("O valor de porosidade deve ser entre 0 e 1")
                except Exception as e:
                    st.error(f"Um erro ocorreu: {e}")

    with st.expander("Correção de Shale"):
        # Abas: Dewan (densidade, sonico neutrao), Schlumberger (densidade, neutrao)
        list_of_tabs_shale_correction = ["Dewan", "Schlumberger"]

        shale_correction_tabs = st.tabs(list_of_tabs_shale_correction)

        with shale_correction_tabs[0]:
            st.write(
                """
                Dewan (1983) propôs uma série de correções para valores de porosidade derivados de logs de densidade, 
                sônico e de nêutrons, levando em consideração o volume de shale e a porosidade correspondente de uma 
                argila adjacente à profundidade de interesse. Para cada tipo de log, Dewan forneceu uma equação específica
                para corrigir a porosidade, considerando a influência do volume de shale e o valor da porosidade na argila próxima.
                """
            )
            st.latex(r"\phi_{cor} = \phi - V_{shale} \cdot \phi_{shale}")
            st.write(
                r"""
                Onde:
                $\phi_{cor}$ - Porosidade pelo perfil de Densidade, Sônico ou Neutrão - corrigido para shale.
                $\phi$ - Porosidade pelo perfil de Densidade, Sônico ou Neutrão
                $\phi_{shale}$ - Porosidade pelos perfis em um shale próximo
                $V_{shale}$ - Volume de Shale 
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
            if st.button("Calcular", key="dewan"):
                try:
                    phi_cor = phi - vshale * phi_shale
                    if log_opts == "Densidade":
                        st.metric(
                            "Porosidade pela Densidade corrigida para Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                    elif log_opts == "Sônico":
                        st.metric(
                            "Porosidade pelo Sônico corrigida para Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                    elif log_opts == "Neutrão":
                        st.metric(
                            "Porosidade pelo Neutrão corrigida para Shale",
                            value=f"{phi_cor:.4g} | {phi_cor*100:.2f}%",
                        )
                except Exception as e:
                    st.warning(f"Um erro ocorreu: {e}")

        with shale_correction_tabs[1]:
            st.write(
                """
                Schlumberger (1975) propôs correções para os valores de porosidade 
                derivados de logs de densidade e de neutrão. Em ambos os casos, as 
                equações incluem o volume de shale e o valor de porosidade de uma 
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
                    $\phi_{De}$ - porosidade do log de densidade corrigida para shale  
                    $\phi_{D}$ - porosidade do log de densidade  
                    $\phi_{DShale}$ - porosidade do log de densidade em um shale adjacente  
                    $V_{shale}$- volume de shale  
                    """
                )
            with cols[1]:
                st.latex(
                    r"\phi_{Ne} = \phi_{N} - \left[(\frac{\phi_{Nshale}}{0.45}) \cdot 0.03 \cdot V_{shale} \right]"
                )
                st.write(
                    r"""
                    Onde:  
                    $\phi_{Ne}$ - porosidade do log de neutrão corrigida para shale  
                    $\phi_{N}$ - porosidade do log de neutrão  
                    $\phi_{NShale}$ - porosidade do log de neutrão em um shale adjacente  
                    $V_{shale}$- volume de shale  
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
                "Calcular (Densidade)"
                if opts_schlumberger == "Densidade"
                else "Calcular (Neutrão)"
            ):
                try:
                    phi_result = phi_dn - (
                        (phi_dnshale / 0.45) * 0.03
                        if opts_schlumberger == "Neutrão"
                        else 0.13 * vshale
                    )
                    st.metric(
                        (
                            "Porosidade corrigida (Densidade)"
                            if opts_schlumberger == "Densidade"
                            else "Porosidade corrigida (Neutrão)"
                        ),
                        f"{phi_result:.4g} | {phi_result*100:.2f}%",
                    )
                except Exception as e:
                    st.warning(f"Um erro ocorreu: {e}")
