import streamlit as st
from components.crystalography import generate_crystal
import components.mineral_id as mineral_id
import components.sidebar as sidebar
import scripts.petrophysics.porosity as porosity
import numpy as np
import matplotlib.pyplot as plt
import scripts.petrophysics.shale_volume as sv
from sympy import symbols

st.set_page_config(
    page_title="PetrofisicaHub",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)
sidebar.show()

st.title("PetrofisicaHub")

tabs_list = [
    "Porosidade",
    "Permeabilidade",
    "Resistividade",
    "Saturação de Água",
    "Volume de Shale",
    "Reservas",
]

tabs = st.tabs(tabs_list)

with tabs[0]:  # Porosidade
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


with tabs[1]:  # Permeabilidade
    st.subheader("Permeabilidade")

    st.write(
        """
        Permeabilidade é a facilidade com que um fluido flui através de um meio poroso. Definida por Darcy, é medida em unidades que levam seu nome. É usada para diferenciar reservatórios convencionais de não convencionais, dependendo do fluido produzido (óleo ou gás).

        A permeabilidade é geralmente calculada em laboratório, testando uma amostra de rocha com diferentes técnicas. Contudo, as medições podem ser imprecisas devido às mudanças nas condições das rochas após a extração.

        Diversas equações foram propostas para calcular a permeabilidade, mas as medições laboratoriais ainda são as mais precisas. Também existem estimativas derivadas de registros de poços por ressonância magnética nuclear (NMR), usadas por algumas empresas para determinar porosidade efetiva a partir do conteúdo de hidrogênio.

        A escolha entre dados laboratoriais ou estimativas derivadas de equações depende do critério do petrofísico ou do especialista em reservatórios.
        """
    )

    with st.expander(
        "Permeabilidade - Wyllie & Rose (1950) - Óleo de Média Densidade",
        icon=":material/landslide:",
    ):
        st.write(
            """
        Wyllie & Rose (1950) desenvolveram uma equação para calcular a permeabilidade em reservatórios de óleos de média densidade. Essa equação leva em consideração os valores de porosidade e saturação de água irredutível, e a expressão é a seguinte: 
        """
        )
        st.latex(r"K = (250 \cdot \frac{\phi^{3}}{Swirr})^{2}")
        st.write(
            r"""
        Onde:  
        - K - Permeabilidade em milidarcy  
        - $\phi$ - Porosidade  
        - Swirr - Saturação de água (Sw) de uma zona com saturação irredutível de água
        """
        )
        cols = st.columns(2)
        with cols[0]:
            phi = st.number_input("Porosidade (decimal)")
        with cols[1]:
            swirr = st.number_input(
                "Saturação de Água em uma zona irredutível (decimal)",
                min_value=0.01,
                max_value=1.00,
            )
        if st.button("Calcular", key=3):
            try:
                K = (250 * ((phi**3) / swirr)) ** 2
                st.success(f"Resultado (mD): {K:.4f}")
            except Exception as e:
                st.warning(f"Ocorreu um erro: {e}")

with tabs[2]:  # Resistividade
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

with tabs[3]:  # Water Saturation
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

with tabs[4]:  # Shale Volume
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

with tabs[5]:  # Oil Reserves
    st.subheader("Reservas")
    st.write(
        """
     O cálculo da porosidade e da saturação de água desempenha um papel importante no momento de estimar as reservas de petróleo e gás, pois um erro considerável ao calcular esses dois valores pode trazer sérios problemas econômicos se estivermos falando de um reservatório gigante.

    O fator de recuperação é outro parâmetro importante nos cálculos de estimativa de reservas, e esse valor dependerá do(s) mecanismo(s) de drenagem natural do reservatório (capa de gás, aquífero, etc.), que são muito diferentes entre eles. Além disso, o fator de recuperação pode aumentar com a aplicação de técnicas de recuperação secundária e terciária no reservatório, mas essa melhoria adiciona mais custos ao orçamento de exploração.  
    """
    )
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
                $N_{f}$ - reservas volumétricas de petróleo recuperáveis em barris de tanque de estoque (STB)
                $7758$ - barris por acre-pé
                $A$ - área de drenagem em acres
                $h$ - espessura do reservatório em pés
                $\phi$ - porosidade (fração decimal)
                $S_{h}$ - saturação de hidrocarbonetos (1-Sw) (fração decimal)
                $RF$ - fator de recuperação
                $B_{oi}$ - fator de volume de óleo, ou barris do reservatório por barril de tanque de estoque

                 """
        )

    with reserve_tabs[1]:
        st.latex(r"B_{oi} = 1.05 + 0.5 \cdot (\frac{GOR}{100})")
        st.write(
            r"""
            $B_{oi}$ - Fator de volume de óleo, ou barris de reservatório por barril em tanque de superfície
            $GOR$ - Razão Óleo-Gás
            """
        )

    with reserve_tabs[2]:
        st.latex(r"GOR = \frac{Gas_{cubic feet}}{Oil_{barrels}}")
