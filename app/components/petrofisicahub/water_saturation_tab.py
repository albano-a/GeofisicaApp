import streamlit as st
import numpy as np
from numpy import sqrt


def render_water_saturation():
    st.subheader("Saturação de Água")
    st.write(
        """
        **Fluid saturation** is the ratio between the volume occupied by a fluid and the total pore volume of the rock:

        **Saturation = fluid volume / pore volume**

        **Water saturation ($S_w$)** indicates how much of the porosity is filled with water. In irreductible water zones, $S_w$ can drop to around **15% in oil-wet rocks**, and remains **above 20% in water-wet rocks** — serving as a reference for validating calculations.

        Sedimentary rocks are typically **water-wet**, whereas **carbonates** often show **mixed or oil-wet wettability**.

        Obtaining a reliable $S_w$ value is essential for accurately **estimating hydrocarbon reserves**. It can be derived using **resistivity and spontaneous potential ($SP$) logs**.
        """
    )
    with st.expander("Water Saturation ($S_w$) - Archie (1942)"):
        st.write(
            """
        Archie's equation is one of the most known ways to calculate water saturation. This author included in his equation different physical rock properties and measurements from different well logs like tortuosity, water and formation resistivities, saturation exponent, and porosity. The equation is the following:
        """
        )
        st.latex(
            r"S_{w} = \left(\frac{  a \cdot R_{w}  }{ R_{t} \cdot \phi^{m} }  \right)^{\frac{1}{n}}"
        )
        st.write(
            r"""
            Onde:

            - $S_{w}$ - Water saturation of the uninvaded zone

            - $R_{t}$ - True formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

            - $R_{w}$ - Resistivity of formation water at formation temperature 

            - $\phi$ - Porosity

            - $a$ - Tortuosity Factor

            - $m$ - Cementation Exponent

            - $n$ - Saturation Exponent
            """
        )
        cols = st.columns(3)
        with cols[0]:
            rt = st.number_input("$R_{t}$ (ohm-m)", min_value=0.0, key="rt_sw_archie")
            a = st.number_input(
                "$a$",
                min_value=0.01,
                help="Degree of deviation of fluid paths from the shortest route.",
                key="fator_tortuosidade_2",
            )

        with cols[1]:
            rw_in = st.number_input(
                "$R_{w}$ (ohm-m)", min_value=0.0, key="rw_sw_archie"
            )
            m = st.number_input(
                "$m$",
                min_value=0.0,
                help="Reflects the compaction and permeability of the rock.",
                key="expoente_cimentacao_2",
            )

        with cols[2]:
            phi = st.number_input(
                r"$\phi$ (decimal)",
                min_value=0.01,
                max_value=1.00,
                key="porosidade_5",
            )
            n = st.number_input("$n$", min_value=0.0, key="n_sw_archie")

        if st.button("Calculate", key=5):
            try:
                if a == 0:
                    st.warning("The tortuosity factor cannot be zero.")
                else:
                    sw_archie = ((a * rw_in) / (rt * (phi**m))) ** (1 / n)
                    st.success(
                        f"Calculated Water Saturation: {sw_archie:.4f} | {sw_archie*100:.2f}%"
                    )
            except Exception as e:
                print("An error occurred: {e}")

    with st.expander("Water Saturation ($S_w$) - Dewan (1983)"):
        sw_dewan_opts = st.radio(
            label="There are two types:",
            options=["Compensated Water Saturation", "Dispersed Clay Model"],
            horizontal=True,
        )
        if sw_dewan_opts == "Compensated Water Saturation":
            st.write(
                """
                Dewan (1983) proposed an equation to calculate compensated water saturation, incorporating key rock and fluid properties such as water resistivity, formation resistivity, and porosity derived from sonic logs. The equation is as follows:
                """
            )
            st.latex(r"S_{w} = 0.9 \cdot \frac{\sqrt{R_{w}/R_{t}}}{\phi_{S}}")
            st.write(
                r"""
                Where:  
                $S_w$ - Water saturation of the uninvaded zone  
                $R_t$ - True formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)  
                $R_w$ - Resistivity of formation water at formation temperature  
                $\phi_{S}$ - Sonic porosity  
                """
            )

            cols = st.columns(2)

            with cols[0]:
                rw = st.number_input(
                    "$R_w$ (ohm-m)", min_value=0.00, key="dewan_comp_sw_1"
                )
                phi_s = st.number_input(
                    r"$\phi_{S}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="dewan_comp_sw_2",
                )

            with cols[1]:
                rt = st.number_input(
                    "$R_t$ (ohm-m)", min_value=0.00, key="dewan_comp_sw_3"
                )

            if st.button("Calculate", key="calc_dewan_comp_sw"):
                try:
                    sw = 0.9 * ((np.sqrt(rw / rt)) / (phi_s))
                    if 0 <= sw <= 1:
                        st.metric("Water Saturation", value=f"{sw:.4g} | {sw*100:.2f}%")
                    else:
                        st.warning(
                            f"The value must be between 0 and 1, right now it's {sw}"
                        )

                except Exception as e:
                    print(f"An error occurred: {e}")

        elif sw_dewan_opts == "Dispersed Clay Model":
            st.write(
                """
                Dewan (1983) also created an equation for the calculation of 
                water saturation for dispersed clay models. This equation includes 
                values such as water and true formation resistivities, sonic derived 
                porosity, and a constant "q" that depends on the density and sonic 
                derived porosity. The expression is the following:
                """
            )
            st.latex(
                r"S_{w} = \frac{\left[  \sqrt{\frac{0.8 \cdot R_{w}}{\phi_{S}^{2} \cdot R_{t}} + (\frac{q}{2})^{2}} - \frac{q}{2} \right]}{(1 - q)}"
            )
            st.write(
                r"""
                Where:  
                $S_w$ - Water saturation of the uninvaded zone  
                $R_t$ - True formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)  
                $R_w$ - Resistivity of formation water at formation temperature  
                $\phi_{S}$ - Sonic porosity  
                $q$ - Intergranular space filled with clay
                """
            )

            cols = st.columns(2)

            with cols[0]:
                rw = st.number_input(
                    "$R_w$ (ohm-m)", min_value=0.00, key="dewan_clay_sw_1"
                )
                phi_s = st.number_input(
                    r"$\phi_{S}$ (decimal)",
                    min_value=0.01,
                    max_value=1.00,
                    key="dewan_clay_sw_2",
                )

            with cols[1]:
                rt = st.number_input(
                    "$R_t$ (ohm-m)", min_value=0.00, key="dewan_clay_sw_3"
                )
                q = st.number_input(r"$q$", min_value=0.00, key="dewan_clay_sw_4")

            if st.button("Calculate", key="calc_dewan_clay_sw"):
                try:
                    root_1 = (0.8 * rw) / (rt * phi_s**2)
                    root_2 = (q / 2) ** 2
                    sw = (np.sqrt(root_1 + root_2) - (q / 2)) / (1 - q)
                    if 0 <= sw <= 1:
                        st.metric("Water Saturation", value=f"{sw:.4g} | {sw*100:.2f}%")
                    else:
                        st.warning(
                            f"The value must be between 0 and 1, right now it's {sw}"
                        )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            tabs = st.tabs(["Constant $q$"])
            with tabs[0]:
                st.write(
                    "Constant q is related to the intergranular space filled with clay, and this depends on the values of density and sonic porosity. The equation to calculate it, is the following:"
                )
                st.latex(r"q = \frac{\phi_{S} - \phi_{D}}{\phi_{S}}")
                st.write(
                    r"""
                    Where:  
                    $\phi_{D}$ - Density porosity  
                    $\phi_{S}$ - Sonic porosity  
                    $q$ - Intergranular space filled with clay
                """
                )
                cols = st.columns(2)
                with cols[0]:
                    phi_s = st.number_input(
                        r"$\phi_{S}$ (decimal)",
                        min_value=0.01,
                        max_value=1.00,
                        key="dewan_q_sw_1",
                    )
                with cols[1]:
                    phi_d = st.number_input(
                        r"$\phi_{D}$ (decimal)",
                        min_value=0.01,
                        max_value=1.00,
                        key="dewan_q_sw_2",
                    )
                if st.button("Calculate", key="calc_dewan_clay_sw"):
                    try:
                        q = (phi_s - phi_d) / phi_s
                        if 0 <= q <= 1:
                            st.metric("Constant $q$", value=f"{q:.4g}")
                        else:
                            st.warning(
                                f"The value must be between 0 and 1, right now it's {q}"
                            )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

    with st.expander("Water Saturation ($S_w$) - Ferlt, Schlumberger and Simandoux"):
        pass
