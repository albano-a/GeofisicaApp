import streamlit as st
import numpy as np


def render_water_saturation():
    st.write(
        """
        **Fluid saturation** is the ratio between the volume occupied by a fluid and the total pore volume of the rock:

        **Saturation = fluid volume / pore volume**

        **Water saturation ($S_w$)** indicates how much of the porosity is filled with water. In irreducible water zones, $S_w$ can drop to around **15% in oil-wet rocks**, and remains **above 20% in water-wet rocks** — serving as a reference for validating calculations.

        Sedimentary rocks are typically **water-wet**, whereas **carbonates** often show **mixed or oil-wet wettability**.

        Obtaining a reliable $S_w$ value is essential for accurately **estimating hydrocarbon reserves**. It can be derived using **resistivity and spontaneous potential ($SP$) logs**.
        """
    )
    with st.expander("Archie (1942)"):
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

    with st.expander("Dewan (1983)"):
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

    with st.expander("Simandoux, Ferlt, and Schlumberger"):
        author_radio = st.radio(
            "Select the author:",
            horizontal=True,
            options=["Simandoux", "Schlumberger", "Ferlt"],
        )

        if author_radio == "Simandoux":

            key_simandoux = "rw_simandoux"
            st.write(
                """
                Another well known equation to calculate water saturation is Simandoux's equation (1963). This uses the same parameters used in other equations from other authors (e.g. Schlumberger, Ferlt, etc.), like shale volume, porosity, water resistivity, true formation resistivity, and shale/clay resistivity. The equation expression is the following:
                """
            )
            st.latex(
                r"""
                S_w = \left(\frac{0.4 \cdot R_w}{\phi^{2}} \right) \cdot \left[  \sqrt{(\frac{V_{shale}}{R_{sh}}) + \frac{5\phi^{2}}{R_{t}R_{w}}} - \frac{V_{shale}}{R_{sh}}  \right]
                """
            )
            st.write(
                r"""
                Where:  
                $S_{w}$ - Water saturation of the uninvaded zone  
                $R_{t}$ - True formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)  
                $R_{w}$ - Resistivity of formation water at formation temperature  
                $\phi$ - Porosity  
                $V_{shale}$ - Shale volume  
                $R_{shale}$ - Shale/clay resistivity value in a formation  
                """
            )
            cols = st.columns(3)
            with cols[0]:
                rw = st.number_input(
                    "$R_{w}$ (ohm-m)", min_value=0.00, key=key_simandoux * 1
                )
                vsh = st.number_input(
                    "$V_{shale}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key=key_simandoux + "2",
                )
            with cols[1]:
                phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key=key_simandoux + "3",
                )
                rsh = st.number_input(
                    "$R_{shale}$ (ohm-m)", min_value=0.00, key=key_simandoux + "4"
                )
            with cols[2]:
                rt = st.number_input("$R_{t}$", min_value=0.00, key=key_simandoux + "5")

            if st.button("Calculate", key=key_simandoux + "6"):
                try:
                    external_eq = (0.4 * rw) / (phi**2)
                    root_1 = (vsh / rsh) ** 2
                    root_2 = (5 * phi**2) / (rt * rw)
                    sw = external_eq * (np.sqrt(root_1 + root_2) - (vsh / rsh))
                    if 0 <= sw <= 1:
                        st.metric("Water Saturation", value=f"{sw:.4g} | {sw*100:.2f}%")
                    else:
                        st.warning(
                            f"The value must be between 0 and 1, right now it's {sw}"
                        )
                except Exception as e:
                    st.write(f"An error occurred: {e}")

        elif author_radio == "Schlumberger":
            key_slb = "sw_schlumberger"
            st.write(
                """
                Schlumberger (1975) also proposed an equation to calculate water saturation. The parameters involved are similar to those in Ferlt's (1975) equation—such as shale volume, porosity, water resistivity, and true formation resistivity—but with one key addition: the resistivity of shale or clay. The equation is shown below:
                """
            )
            st.latex(
                r"""
                S_w = 
                \frac{\sqrt{
                \left(\frac{V_{\text{shale}}}{R_{\text{sh}}}\right)^2 + \frac{\phi^2}{0.2 \cdot R_w \cdot R_t \cdot (1 - V_{\text{shale}})} - \frac{V_{\text{shale}}}{R_{\text{sh}}}
                }}{
                \frac{\phi^2}{0.4 \cdot R_w \cdot (1 - V_{\text{shale}})}
                }
                """
            )
            st.write(
                r"""
                Where:  
                $S_w$ - water saturation of the uninvaded zone  
                $R_t$ - true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)  
                $R_w$ - resistivity of formation water at formation temperature  
                $\phi$  - porosity  
                $V_{shale}$ - shale volume  
                $R_{shale}$ - shale/clay resistivity value in a formation  
                """
            )

            cols = st.columns(3)
            with cols[0]:
                rw = st.number_input("$R_{w}$ (ohm-m)", min_value=0.00, key=key_slb * 1)
                vsh = st.number_input(
                    "$V_{shale}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key=key_slb + "2",
                )
            with cols[1]:
                phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key=key_slb + "3",
                )
                rsh = st.number_input(
                    "$R_{shale}$ (ohm-m)", min_value=0.00, key=key_slb + "4"
                )
            with cols[2]:
                rt = st.number_input("$R_{t}$", min_value=0.00, key=key_slb + "5")

            if st.button("Calculate", key=key_slb + "6"):
                try:
                    # numerator
                    term1 = (vsh / rsh) ** 2
                    term2 = (phi**2) / (0.2 * rw * rt * (1 - vsh))
                    term3 = vsh / rsh
                    num = term1 + term2 - term3
                    # denominator
                    den = (phi**2) / (0.4 * rw * (1 - vsh))

                    sw = num / den
                    if 0 <= sw <= 1:
                        st.metric("Water Saturation", value=f"{sw:.4g} | {sw*100:.2f}%")
                    else:
                        st.warning(
                            f"The value must be between 0 and 1, right now it's {sw}"
                        )
                except Exception as e:
                    st.write(f"An error occurred: {e}")

        elif author_radio == "Ferlt":
            key_ferlt = "sw_ferlt"
            st.write(
                """
                One of the equations used to calculate water saturation is Ferlt's equation (1975). It incorporates porosity, water resistivity, true formation resistivity, shale volume, and a constant "a", whose value is known for specific geological zones. The equation is as follows:
                """
            )
            st.latex(
                r"""
                S_w = \frac{1}{\phi} \cdot \left(
                {
                    \sqrt{
                        \frac{R_w}{R_t} + \left(\frac{a \cdot V_{shale}}{2}\right)^{2}    
                    } - 
                    \frac{a \cdot V_{shale}}{2}
                }\right)
                """
            )
            st.write(
                r"""
                Where:  
                $S_w$ - Water saturation of the uninvaded zone  
                $R_t$ - True formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)  
                $R_w$ - Resistivity of formation water at formation temperature  
                $\phi$ - Porosity  
                $V_{shale}$ - Shale volume  
                $a$ - $0.25$ at the Golf Coast  
                $a$ - $0.35$ at the Rocky Mountains
                """
            )

            cols = st.columns(3)
            with cols[0]:
                rw = st.number_input(
                    "$R_{w}$ (ohm-m)", min_value=0.00, key=key_ferlt * 1
                )
                vsh = st.number_input(
                    "$V_{shale}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key=key_ferlt + "2",
                )
            with cols[1]:
                phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key=key_ferlt + "3",
                )
                a = st.number_input("$a$", min_value=0.00, key=key_ferlt + "4")
            with cols[2]:
                rt = st.number_input("$R_{t}$", min_value=0.00, key=key_ferlt + "5")

            if st.button("Calculate", key=key_ferlt + "6"):
                try:
                    root1 = rw / rt
                    root2 = ((a * vsh) / 2) ** 2
                    term1 = np.sqrt(root1 + root2)
                    term2 = (a * vsh) / 2

                    sw = (1 / phi) * (term1 - term2)
                    if 0 <= sw <= 1:
                        st.metric("Water Saturation", value=f"{sw:.4g} | {sw*100:.2f}%")
                    else:
                        st.warning(
                            f"The value must be between 0 and 1, right now it's {sw}"
                        )
                except Exception as e:
                    st.write(f"An error occurred: {e}")
