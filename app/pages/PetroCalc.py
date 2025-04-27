import streamlit as st
from components.crystalography import generate_crystal
import components.mineral_id as mineral_id
import components.sidebar as sidebar
import scripts.petrophysics.porosity as porosity

st.set_page_config(
    page_title="PetroCalc",
    page_icon="assets/geofisicahub_favicons.svg",
    layout="centered",
)
sidebar.show()

st.title("PetroCalc")

tabs_list = [
    "Porosidade",
    "Permeabilidade",
    "Resistividade",
    "Saturação de Água",
    "Volume de Shale",
    "Reservas",
]

tabs = st.tabs(tabs_list)

with tabs[0]:
    st.subheader("Porosidade")

    st.write(
        r"""
        Porosidade é um importante parâmetro petrofísico da rocha, que é definido como a relação entre o volume dos poros da rocha e o volume total da rocha.

        $\text{Porosidade} = \frac{V_{\text{poros}}}{V_{\text{total}}}$

        Essa propriedade física limita a rocha no momento de acumular hidrocarbonetos (óleo, condensados ou gás), porém, a porosidade deve estar interconectada para adicionar valor comercial a um reservatório. Existem porosidade total e porosidade efetiva, onde a primeira está relacionada a todos os poros de uma rocha, e a segunda, apenas aos poros interconectados, que são mais importantes no momento da produção de hidrocarbonetos.
        Além disso, o volume de folhelho afeta a qualidade dos reservatórios, e é por isso que correções têm que ser feitas ao calcular a porosidade, conhecidas como valores corrigidos para folhelho. 
        """
    )

    with st.expander("Porosidade por Densidade", icon=":material/landslide:"):
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
        cols = st.columns(2)
        with cols[0]:
            rho_log = st.number_input("Densidade Bulk do Perfil")
        with cols[1]:
            rho_matrix = st.number_input("Densidade da Matriz")
        rho_fluid = st.number_input("Densidade do Fluido")

        if st.button("Calcular", key=1):
            try:
                result = porosity.density_porosity(rho_log, rho_matrix, rho_fluid)
                st.success(f"Porosidade calculada: {result:.4f} | {result*100:.2f}%")
            except Exception as e:
                st.warning(e)

    with st.expander("Porosidade Densidade-Neutrão", icon=":material/landslide:"):
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
            phid = st.number_input("Porosidade efetiva a partir da Densidade (decimal)")
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
                st.success(f"Porosidade calculada: {result:.4f} | {result*100:.2f}%")
            except Exception as e:
                st.warning(e)

with tabs[1]:
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

with tabs[2]:
    st.subheader("Resistividade")

    st.write(
        """
         Resistividade é definida como a oposição ou resistência que um material tem para interferir no fluxo de uma corrente elétrica. No caso das rochas sedimentares, estas contêm fluidos em seus poros que têm diferentes tipos de resistividades.

        Um volume de poros da rocha pode conter igualmente óleo, gás ou água. Óleo e gás têm um valor de resistividade mais alto do que a água, o que permite detectar a presença de hidrocarbonetos em um poço usando ferramentas de registro de resistividade, por exemplo.

        No entanto, a salinidade da água também afeta a resistividade da água, e ela pode ter uma ampla gama de valores. A água salgada tem uma resistividade menor do que a água doce, portanto, tem um valor de resistividade mais baixo.

        Além de ajudar a detectar a presença de hidrocarbonetos, a resistividade da água é amplamente utilizada para o cálculo da saturação de água, que é um valor muito importante na estimativa de reservas de hidrocarbonetos. 
        """
    )

    with st.expander("Resistividade da Água Rw - Archie"):
        st.write(
            """
         Uma das formas mais conhecidas de calcular a saturação de água é por meio da equação de Archie. Essa equação leva em consideração medições e valores como a resistividade da formação saturada com água, porosidade, fator de tortuosidade e o expoente de cimentação. A equação expressa é a seguinte:
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

            - $ɸ$ - Porosidade
            
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

with tabs[3]:
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

with tabs[4]:
    st.subheader("Volume de Shale")
    
    st.write(
        """
        O volume de argila é um valor fundamental para avaliar a qualidade de uma rocha reservatório.

        De acordo com o volume de argila que uma rocha reservatório possui, será determinado o quão explorável um reservatório é ou não.

        Existem diferentes métodos para calcular o volume de argila, onde podemos citar algumas dessas equações: Larionov, Larionov-rochas antigas, Steiber, Clavier. Algumas dessas equações utilizam os valores de registro de poço de raio gama, e algumas delas utilizam valores da ferramenta de registro de potencial espontâneo (SP).

        Além disso, esse valor é usado para fazer correção de argila para valores de porosidade derivados de diferentes ferramentas de registro de poços, para que possamos ter um valor de porosidade mais confiável. 
        """
    )

    with st.expander("Índice de GR"):
        st.write(
            """
        O **Índice de Gamma Ray (IGR)** é calculado a partir da ferramenta de registro geofísico que tem o mesmo nome. Esse índice leva em consideração o valor mínimo de gamma ray (zona mais limpa), o valor máximo de gamma ray (zona mais argilosa) e o valor da área ou profundidade de estudo. 
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
        
        O índice de gamma ray é o ponto de partida para calcular o volume de argila a partir de diferentes equações de diversos autores.
        """
        )
        cols = st.columns(2)
        with cols[0]:
            gr_log = st.number_input(r"Leitura de GR ($\text{GR}_{log}$)")

        with cols[1]:
            gr_min = st.number_input(r"Valor Mínimo de GR ($\text{GR}_{min}$)")
        gr_log_2 = st.file_uploader(
            "Ou importe o seu .las aqui",
            type=".las",
            help="Ao fazer o upload, o .LAS será lido e a provável curva de GR será encontrada",
        )
        gr_max = st.number_input(r"Valor Máximo de GR ($\text{GR}_{max}$)")

        if st.button("Calcular IGR"):
            try:
                if gr_max == gr_min:
                    st.warning("GR_max e GR_min não podem ser iguais.")
                else:
                    igr = (gr_log - gr_min) / (gr_max - gr_min)
                    st.success(
                        f"Índice de Gamma Ray calculado: {igr:.4f} | {igr*100:.2f}"
                    )
            except Exception as e:
                st.warning(f"Ocorreu um erro: {e}")

with tabs[5]:
    st.subheader("Reservas")
    st.write(
        """
     O cálculo da porosidade e da saturação de água desempenha um papel importante no momento de estimar as reservas de petróleo e gás, pois um erro considerável ao calcular esses dois valores pode trazer sérios problemas econômicos se estivermos falando de um reservatório gigante.

    O fator de recuperação é outro parâmetro importante nos cálculos de estimativa de reservas, e esse valor dependerá do(s) mecanismo(s) de drenagem natural do reservatório (capa de gás, aquífero, etc.), que são muito diferentes entre eles. Além disso, o fator de recuperação pode aumentar com a aplicação de técnicas de recuperação secundária e terciária no reservatório, mas essa melhoria adiciona mais custos ao orçamento de exploração.  
    """
    )

    with st.expander("Reservas de Petróleo"):
        st.latex(
            r"N_{f} = \frac{7758 \cdot A \cdot h \cdot \phi \cdot S_{h} \cdot FR}{B_{oi}}"
        )
        st.write(
            r"""
                 - $N_{f}$ - reservas volumétricas de petróleo recuperáveis em barris de tanque de estoque (STB)
                - $7758$ - barris por acre-pé
                - $A$ - área de drenagem em acres
                - $h$ - espessura do reservatório em pés
                - $\phi$ - porosidade (fração decimal)
                - $S_{h}$ - saturação de hidrocarbonetos (1-Sw) (fração decimal)
                - $RF$ - fator de recuperação
                - $B_{oi}$ - fator de volume de óleo, ou barris do reservatório por barril de tanque de estoque

                 """
        )
