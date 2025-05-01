import streamlit as st
import scripts.petrophysics.porosity as porosity
import scripts.petrophysics.shale_volume as sv
import numpy as np


def render_permeability():
    st.subheader("Permeability")

    st.write(
        """
        Permeability refers to the ease with which a fluid flows through a porous medium. Defined by Darcy, it is measured in units bearing his name. It serves to differentiate conventional from unconventional reservoirs, based on the produced fluid (oil or gas).

        Permeability is typically calculated in the laboratory by testing a rock sample using various techniques. However, these measurements can be imprecise due to changes in the rock's conditions after extraction.

        Several equations have been proposed to calculate permeability, but laboratory measurements remain the most accurate. Estimates derived from nuclear magnetic resonance (NMR) well logs also exist and are used by some companies to determine effective porosity from hydrogen content.

        The choice between laboratory data and estimates derived from equations depends on the criteria of the petrophysicist or reservoir specialist.
        """
    )
    key_mgo = "mgo_calc"
    key_dg = "dg_calc"

    with st.expander("Wyllie & Rose (1950)"):
        radio_calcs = st.radio(
            "Select type of equation:",
            ["Medium Gravity Oil", "Dry Gas"],
            horizontal=True,
        )
        if radio_calcs == "Medium Gravity Oil":
            st.write(
                """
            Wyllie & Rose (1950) developed an equation to calculate permeability in medium gravity oil reservoirs. This equation takes into account porosity and irreducible water saturation values, and the expression is as follows:
            """
            )
            st.latex(r"K = (250 \cdot \frac{\phi^{3}}{Swirr})^{2}")
        else:
            st.write(
                """
            Wyllie & Rose (1950) also proposed an equation to calculate permeability in dry gas reservoirs, where like in the case of medium gravity oil reservoirs, this equation considers the values of porosity and irreducible water saturation. The equation is the following one:
            """
            )
            st.latex(r"K = (73 \cdot \frac{\phi^{3}}{Swirr})^{2}")
        st.write(
            r"""
        Onde:  
        - K - Permeability in milidarcy  
        - $\phi$ - Porosity  
        - Swirr - Water saturation (Sw) of a zone at irreducible water saturation
        """
        )
        cols = st.columns(2)
        with cols[0]:
            phi = st.number_input(
                r"$\phi$ (decimal)", min_value=0.00, max_value=1.00, key=key_mgo
            )
        with cols[1]:
            swirr = st.number_input(
                r"$Swirr$ (decimal)",
                min_value=0.01,
                max_value=1.00,
                key=key_mgo * 2,
            )
        if st.button("Calculate", key=key_mgo * 3):
            try:
                constant = 250 if radio_calcs == "Medium Gravity Oil" else 73

                K = (constant * ((phi**3) / swirr)) ** 2
                st.metric("Permeability", value=f"{K:.4f} mD")
            except Exception as e:
                st.warning(f"An error occurred: {e}")

    with st.expander("Timur (1968)"):
        st.write(
            """
            Timur (1968) also proposed an equation for permeability calculation. It is an expression similar to the Wyllie & Rose (1950) equation, which considers the porosity and the irreducible water saturation values, but Timur did not differentiate the fluid type accumulated in the reservoir. The equation is the following:
            """
        )
        st.latex(r"K = \left( \frac{93 \cdot \phi^{2.2}}{S_{wirr}} \right)^{2}")
        st.write(
            r"""
            Where:  
            $K$ - Permeability in milidarcys  
            $\phi$ - Porosity  
            $S_{wirr}$ - Water saturation of a zone at irreducible water saturation
            """
        )
        cols = st.columns(2)

        with cols[0]:
            phi = st.number_input(
                r"$\phi$ (decimal)", min_value=0.00, max_value=1.00, key="timur_perm_1"
            )
        with cols[1]:
            swirr = st.number_input(
                r"$S_{wirr} (decimal)$",
                min_value=0.00,
                max_value=1.00,
                key="timur_perm_2",
            )

        if st.button("Calculate", key="timur_perm_3"):
            try:
                K = ((93 * phi ** (2.2)) / (swirr)) ** 2
                st.metric("Permeability", value=f"{K:.4f}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    with st.expander("Coates & Dumanoir (1973)"):
        cd_tabs = st.tabs(["Permeability", "Constant $W$", "Constant $C$"])

        with cd_tabs[0]:
            st.write(
                """
                Coates & Dumanoir (1973) proposed a more expression for permeability calculation. This equation includes water resistivity and water resistiviy of a formation at an irreducible water saturation zone values, and some constants that are related to resistivity and density values. The equation is the following:
                """
            )
            st.latex(
                r"K = \left( \frac{C \cdot \phi^{2W}}{W^{4} \cdot (R_{w}/R_{tirr})} \right)^{2}"
            )
            st.write(
                r"""
                Where:
                $K$ - Permeability in milidarcys
                $R_w$ - Formation water resistivity at formation temperature
                $R_{tirr}$ - True formation resistivity from a formation at irreducible water saturation (Swirr)
                $\phi$ - Porosity
                $C$ - Coates and Dumanoir constant
                $W$ - Coates and Dumanoir constant
                """
            )
            cols = st.columns(3)
            with cols[0]:
                rw = st.number_input(
                    "$R_w$ (ohm-m)", min_value=0.00, key="coates_perm_1"
                )
                W = st.number_input("$W$", min_value=0.0, key="coates_perm_4")

            with cols[1]:
                rtirr = st.number_input(
                    "$R_{tirr}$ (ohm-m)", min_value=0.00, key="coates_perm_2"
                )
                C = st.number_input("$C$", min_value=0.0, key="coates_perm_5")

            with cols[2]:
                phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="coates_perm_3",
                )

            if st.button("Calculate", key="coates_perm_6"):
                try:
                    num = C * phi ** (2 * W)
                    den = W**4 * (rw / rtirr)
                    K = (num / den) ** 2
                    st.metric("Permeability", value=f"{K:.4f} mD")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        with cd_tabs[1]:
            st.write(
                """
                Constant W of the Coates & Dumanoir equation, is calculated considering porosity and resistivity values, and it is the following:
                """
            )
            st.latex(
                r"""
                W = \left[
                    (3.75 - \phi) +
                    \left[
                        \frac{
                            (\log(R_w/R_{tirr}) + 2.2)^{2}
                        }{
                            2.0
                        }
                    \right]
                \right]^{1/2}
                """
            )
            st.write(
                r"""
                Where:
                $R_w$ - Formation water resistivity at formation temperature
                $R_{tirr}$ - True formation resistivity from a formation at irreducible water saturation (Swirr)
                $\phi$ - Porosity
                """
            )
            cols = st.columns(3)

            with cols[0]:
                phi = st.number_input(
                    r"$\phi$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="w_coates_perm_1",
                )

            with cols[1]:
                rw = st.number_input(
                    r"$R_w$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="w_coates_perm_2",
                )

            with cols[2]:
                rtirr = st.number_input(
                    r"$R_{tirr}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="w_coates_perm_3",
                )

            if st.button("Calculate", key="w_coates_perm_4"):
                try:
                    factor1 = 3.75 - phi
                    num = (np.log10(rw / rtirr) + 2.2) ** 2
                    den = 2.0
                    W = (factor1 + (num / den)) ** (1 / 2)
                    st.metric("Constant W", value=f"{W}")
                except Exception as e:
                    st.write(f"An error occurred: {e}")

        with cd_tabs[2]:
            st.write(
                """
                In the case of constant C, this is calculated from the following expression, which only considers the hydrocarbon density value:
                """
            )
            st.latex(
                r"""
                C = 23 + 465 \cdot \rho_h - 188 \cdot \rho_{h}^{2}
                """
            )
            st.write(
                r"""
                Where:
                \rho_h - Hydrocarbon density in g / cm3
                """
            )
            cols = st.columns(3)

            with cols[1]:
                rho_h = st.number_input(
                    r"$\rho_{h}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="c_coates_perm_1",
                )

            if st.button("Calculate", key="c_coates_perm_2"):
                try:
                    C = 23 + 465 * rho_h - 188 * rho_h**2
                    st.metric("Constant C", value=f"{C}")
                except Exception as e:
                    st.write(f"An error occurred: {e}")

    with st.expander("NMR"):
        tabs = st.tabs(["Normal Model", "Coates Model"])

        with tabs[0]:
            st.write(
                """
                It is also possible to calculate permability from nuclear magnetic resonance well logs (NMR). The equation for the calculation of NMR-derived permeability, includes a constant that depends of the formation type, NMR derived porosity, and T2 distribution. The expression is the following:
                """
            )
            st.latex(r"K = a(\phi_{NMR})^{4}(T_{2gm})^{2}")
            st.write(
                r"""
                Where:  
                $K$ - NMR-derived permeability  
                $a$ - A constant, depending on formation  
                $\phi_{NMR}$ - NMR-derived effective porosity  
                $T_{2gm}$ - Geometric mean of the T2 distribution   
                """
            )
            cols = st.columns(3)

            with cols[0]:
                a = st.number_input(r"$a$", min_value=0.00, key="nmr_1")

            with cols[1]:
                phi_nmr = st.number_input(
                    r"$\phi_{nmr}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="nmr_2",
                )

            with cols[2]:
                t2gm = st.number_input(r"$T_{2gm}$", min_value=0.00, key="nmr_3")

            if st.button("Calculate", key="nmr_4"):
                try:
                    K = a * (phi_nmr**4) * (t2gm**2)
                    st.metric("Permeability", value=f"{K:.4f} mD")
                except Exception as e:
                    st.write(f"An error occurred: {e}")

        with tabs[1]:
            st.write(
                """
                The autor Coates, proposed an equation known as the "three-fluid model", based on nuclear magnetica resonance well log (NMR). This equation considers the NMR derived porosity, and some constants that depend on the formation type, and the proportion of fluids filling the reservoir pores. The equation is the following:
                """
            )
            st.latex(
                r"K = \left(\frac{\phi_{NMR}}{C}\right)^{4}\left(\frac{FFI}{BVI}\right)^{2}"
            )
            st.write(
                r"""
                Where:  
                $K$ - NMR-derived permeability  
                $\phi_{NMR}$ - NMR-derived effective porosity  
                $C$ - Constant, depending on formation  
                $FFI$ - Proportion of moveable fluids occupying effective porosity  
                $BVI$ - Proportion of capillary-bound fluids occupying effective porosity  
                """
            )
            cols = st.columns(2)

            with cols[0]:
                C = st.number_input(r"$C$", min_value=0.00, key="nmr_coates_1")
                FFI = st.number_input(r"$FFI$", min_value=0.00, key="nmr_coates_3")

            with cols[1]:
                phi_nmr = st.number_input(
                    r"$\phi_{nmr}$ (decimal)",
                    min_value=0.00,
                    max_value=1.00,
                    key="nmr_coates_2",
                )
                BVI = st.number_input(r"$BVI$", min_value=0.00, key="nmr_coates_4")

            if st.button("Calculate", key="nmr_coates_5"):
                try:
                    K = ((phi_nmr / C) ** 4) * ((FFI / BVI) ** 2)
                    st.metric("Permeability", value=f"{K:.4f} mD")
                except Exception as e:
                    st.write(f"An error occurred: {e}")
