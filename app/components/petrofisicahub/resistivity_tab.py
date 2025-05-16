import streamlit as st
import numpy as np


def render_resistivity():
    st.write(
        """
        Resistivity is defined as the opposition or resistance that a material has to interfere with 
        the flow of an electric current. In the case of sedimentary rocks, these contain fluids in their 
        pores that have different types of resistivities.

        A rock pore volume may equally contain oil, gas, or water. Oil and gas have a higher resistivity 
        value than water, which allows the detection of hydrocarbons in a well using resistivity logging 
        tools, for example.

        However, the salinity of the water also affects its resistivity, and it can have a wide 
        range of values. Saltwater has a lower resistivity than freshwater, therefore, it has a 
        lower resistivity value.

        In addition to helping detect the presence of hydrocarbons, water resistivity is widely 
        used for the calculation of water saturation, which is a very important value in 
        hydrocarbon reserve estimation.
        """
    )

    with st.expander(r"Water Resistivity $R_{w}$/$R_{wa}$ - Archie"):
        st.write(
            r"""
        One of the best-known ways to calculate water saturation is through the Archie equation, which can be used for both resistivity and apparent resistivity. The difference between the two equations is that for resistivity, the formation resistivity is used, and for apparent resistivity, the true formation resistivity is used, obtained from a deep resistivity log.
        """
        )
        st.latex(
            r"""
            R_{w} = \frac{R_{o} \cdot \phi^{m}}{a}\space\text{or}\space R_{wa} = \frac{R_{t} \cdot \phi^{m}}{a}
                 """
        )
        st.write(
            r"""
         Where:
            - $R_w/R_{wa}$ - Water Resistivity/Apparent Water Resistivity
                        
            - $R_{o}$ - Formation resistivity saturated with water
            
            - $R_{t}$ - True formation resistivity obtained from a deep resistivity log

            - $\phi$ - Porosity / $m$ - Cementation exponent / $a$ - Tortuosity factor

        """
        )
        list_rest_opts = [
            r"Resistivity - $R_w$",
            r"Apparent Resistivity - $R_{wa}$",
        ]
        res_opts = st.radio(
            "Type",
            [r"Resistivity - $R_w$", r"Apparent Resistivity - $R_{wa}$"],
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
                help="Reflects the compaction and permeability of the rock.",
                key="expoente_cimentacao_1",
            )
        with cols[1]:
            phi = st.number_input(r"$\phi$ (decimal)", min_value=0.01, max_value=1.00)
            a = st.number_input(
                "$a$",
                min_value=0.01,
                help="Degree of deviation of fluid paths from the shortest path, due to pore geometry.",
                key="fator_tortuosidade_1",
            )
        if st.button("Calculate", key=4):
            try:
                if a == 0:
                    st.warning("The tortuosity factor cannot be zero.")
                else:
                    rw = (ro * phi**m) / a
                    st.metric(
                        (
                            "Water Resistivity"
                            if res_opts == list_rest_opts[0]
                            else "Apparent Water Resistivity"
                        ),
                        value=f"{rw:.4f} ohm-m",
                    )
            except Exception as e:
                st.warning(f"An error occurred: {e}")

    with st.expander("Water Resistivity - Western Atlas (1985)"):
        st.write(
            r"""
            Western Atlas (1985) proposed an equation for calculating water resistivity ($R_w$), composed of mathematical expressions and values such as the equivalent water resistivity ($R_{we}$) and the bottom hole temperature ($\text{BHT}$). The equation is as follows:
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
                    st.warning("The tortuosity factor cannot be zero.")
                else:
                    rw = (rwe + 0.131 * 10 ** ((1 / (np.log10(bht / 19.9))) - 2)) / (
                        -0.5 * rwe + 10 ** (0.0426 / np.log10(bht / 50.8))
                    )
                    if rw < 0:
                        st.error("Something is wrong, the result cannot be negative.")
                    else:
                        st.metric(
                            "Water Resistivity",
                            value=f"{rw:.4f} ohm-m",
                        )
            except Exception as e:
                st.warning(f"An error occurred: {e}")

        list_western_atlas_tabs = [
            r"Equivalent Water Resistivity ($R_{we}$)",
            r"Filtrate Resistivity ($R_{mf}$)",
            r"Formation Temperature ($T_{f}$)",
        ]

        wes_at_tabs = st.tabs(list_western_atlas_tabs)

        with wes_at_tabs[0]:
            st.latex(r"R_{we} = R_{mf} \cdot 10^{ {SP}/{61 + 0.133\text{BHT}}}")
            st.write(
                r"""
                $R_{mf}$ - Mud Filtrate Resistivity at Formation Temperature  
                $\text{BHT}$ - Bottom Hole Temperature  
                $SP$ - Spontaneous Potential Measurement
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
                        "Equivalent Water Resistivity", value=f"{rwe:.4f} ohm-m"
                    )
                except Exception as e:
                    st.warning(f"An error occurred: {e}")

        with wes_at_tabs[1]:
            st.latex(r"R_{mf} = \frac{R_{mfsurf}(T_{surf}+6.77)}{T_{f} + 6.77}")
            st.write(
                r"""
                $R_{mf}$ - Mud filtrate resistivity at formation temperature
                $R_{mfsurf}$ - Mud filtrate resistivity at measured temperature
                $T_{surf}$ - Temperature at which $R_{mf}$ was measured (surface temperature)
                $T_{f}$ - Formation Temperature
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
                        "Equivalent Water Resistivity", value=f"{rmf:.4f} ohm-m"
                    )
                except Exception as e:
                    st.warning(f"An error occurred: {e}")
        with wes_at_tabs[2]:
            st.latex(r"T_{f} = \left(\frac{BHT - AMST}{TD} \cdot FD \right) + AMST")
            st.write(
                """
                $AMST$ - Annual Mean Surface Temperature  
                $TD$ - Total Depth  
                $BHT$ - Bottom Hole Temperature  
                $T_{f}$ - Formation Temperature  
                $FD$ - Formation Depth  
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
                    st.metric("Formation Temperature", value=f"{tf:.2f} ºF")
                except:
                    print("An exception occurred")

    with st.expander("Water Resistivity - SP Log"):
        st.write(
            """
            Water resistivity (Rw) can also be calculated from the well's spontaneous potential (SP) log. This equation requires the values of mud filtrate resistivity, an SP measurement, and a constant K that depends on the formation temperature. The equation is as follows:
            """
        )
        st.latex(r"R_w = 10^{(K \cdot \log(R_{mf}) + SP) / K}")
        st.write(
            r"""
            Where:
            $R_{w}$ - Water Resistivity
            $R_{mf}$ - Mud Filtrate Resistivity at Formation Temperature
            $K$ - Constant
            $SP$ - Spontaneous Potential
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
                st.metric("Water Resistivity", value=f"{rw_output:.4f} ohm-m")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        k_tab = st.tabs(["Constant $K$"])
        with k_tab[0]:
            st.write(
                """
                To calculate the constant K, it is necessary to know the formation temperature, and the expression is as follows:
                """
            )
            st.latex(r"K = (0.133 \cdot T_{f}) + 60")
            st.write("$T_{f}$ - Formation Temperature")

            cols = st.columns(3)
            with cols[1]:
                tf = st.number_input("$T_{f} (ºF)$", min_value=0.00)

            if st.button("Calculate", key="sp-log-tf"):
                try:
                    K = (0.133 * tf) + 60
                    st.metric("Constant K", value=f"{K}")
                except:
                    print("An exception occurred")

    with st.expander("Total Resistivity"):
        st.write(
            r"""
            The total resistivity ($R_t$) can be calculated using the Archie equation. This equation is composed of the values of water resistivity ($R_w$), tortuosity factor ($a$), porosity ($\phi$), and the cementation ($m$) and saturation ($n$) exponents. The expression is as follows:
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
                st.metric("Total Resistivity", value=f"{rt:.4f}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
