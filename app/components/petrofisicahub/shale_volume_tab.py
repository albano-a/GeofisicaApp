import streamlit as st
import scripts.petrophysics.shale_volume as sv


def render_shale_volume():

    st.write(
        """
        The shale volume (shale) is a fundamental value for evaluating the quality of a reservoir rock. According to the shale volume that a reservoir rock possesses, it will be determined how explorable a reservoir is.

        There are different methods to calculate the shale volume: Larionov, Larionov-old rocks, Steiber, Clavier. Some of these equations use gamma ray log values, and some of them use values from the spontaneous potential (SP) log tool.

        Furthermore, this value is used to make clay corrections for porosity values derived from different well logging tools, so that a more reliable porosity value can be obtained.
        """
    )

    with st.expander("Gamma Ray Index"):
        st.write(
            """
        The **GR index (IGR)** is calculated from the geophysical log tool that has the same name. This index takes into account the minimum gamma ray value (cleanest zone), the maximum gamma ray value (most shaly zone), and the value of the area or depth of study.
        """
        )
        st.latex(r"I_{GR}=\frac{ GR_{log} - GR_{min} }{ GR_{max} - GR_{min} }")
        st.write(
            r"""
         Where:
         $I_{GR}$ - GR index
         $GR_{log}$ - Gamma ray reading of the formation
         $GR_{min}$ - Minimum gamma ray value (clean sand or carbonate)
         $GR_{max}$ - Maximum gamma ray value (shale)

        The GR index is the starting point to calculate the shale volume from different equations by various authors.
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

        if st.button("Calculate IGR"):
            try:
                if gr_max == gr_min:
                    st.warning("GR max and GR min cant be equal.")
                else:
                    igr = (gr_log - gr_min) / (gr_max - gr_min)
                    st.metric(label="GR index", value=f"{igr:.4g} | {igr*100:.2f}%")
            except Exception as e:
                st.warning(f"An error occurred: {e}")

    with st.expander("Larionov (1969)"):
        tab1, tab2 = st.tabs(["Larionov", "Larionov Old Rocks"])
        with tab1:
            st.write(
                """
                The Larionov (1969) equation for Cenozoic rocks (previously known as Tertiary rocks) used for calculating shale volume is as follows:
                """
            )
            st.latex(r"V_{sh} = 0.083 \cdot (2^{3.7 \cdot I_{GR}} - 1)")
            st.write(
                r"""
                Onde:  
                $I_{GR}$ - GR index  
                $V_{sh}$ - Shale volume  
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
            if st.button("Calculate", key="larionov"):
                try:
                    vsh = sv.larionov(igr)
                    st.metric(
                        label="Shale Volume",
                        value=f"{vsh:.4g} | {vsh*100:.2f}%",
                    )
                except Exception as e:
                    st.warning("An error occurred: {e}")

        with tab2:
            st.write(
                """
            Larionov (1969) also proposed an equation for calculating the shale volume in rocks older than the Cenozoic Era, expressed as follows:
            """
            )
            st.latex(r"V_{sh} = 0.33 \cdot (2^{2 \cdot I_{GR}} - 1)")
            st.write(
                r"""
                Onde:  
                $I_{GR}$ - GR index  
                $V_{sh}$ - Shale volume  
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
            if st.button("Calculate", key="larionov_old_rocks"):
                try:
                    if igr <= 1.00 and igr > 0.00:
                        vsh = sv.larionov_old_rocks(igr)
                        st.metric(
                            label="Shale Volume",
                            value=f"{vsh:.4g} | {vsh*100:.2f}%",
                        )
                    else:
                        st.warning(
                            r"$I_{GR}$ must be greater than zero and less than one."
                        )
                except Exception as e:
                    st.warning("An error occurred: {e}")

    with st.expander("Steiber (1970)"):
        st.write(
            """
            Steiber (1970) também propôs uma equação para o cálculo do Shale volume, expressa da seguinte forma:
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
            $I_{GR}$ - GR index  
            $V_{sh}$ - Shale volume  
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
        if st.button("Calculate", key="steiber"):
            try:
                if igr <= 1.00 and igr > 0.00:
                    vsh = sv.steiber(igr)
                    st.metric(
                        label="Shale Volume",
                        value=f"{vsh:.4g} | {vsh*100:.2f}%",
                    )
                else:
                    st.warning(r"$I_{GR}$ must be greater than zero and less than one.")
            except Exception as e:
                st.warning("An error occurred: {e}")

    with st.expander("Clavier (1971)"):
        st.write(
            """
            Clavier (1971) proposed an equation for calculating shale volume, with a more complex expression compared to other authors, 1  presented as follows:
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
            $I_{GR}$ - GR Index  
            $V_{sh}$ - Shale volume  
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
        if st.button("Calculate", key="clavier"):
            try:
                if igr <= 1.00 and igr > 0.00:
                    vsh = sv.clavier(igr)
                    st.metric(
                        label="Shale Volume",
                        value=f"{vsh:.4g} | {vsh*100:.2f}%",
                    )
                else:
                    st.warning(r"$I_{GR}$ must be greater than zero and less than one.")
            except Exception as e:
                st.warning("An error occurred: {e}")

    with st.expander("Shale Volume - SP"):
        tab1, tab2 = st.tabs(["Clássica", "Alternativa"])
        with tab1:
            st.write(
                """
                From the spontaneous potential (SP) log, it is possible to calculate the shale volume using two different equations. The first expression is as follows:
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
                $V_{sh}$ - Shale volume  
                $PSP$ - Pseudostatic spontaneous potential (maximum SP of the clay formation)  
                $SSP$ - Static spontaneous potential of a clean and thick sandstone layer nearby  
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
            if st.button("Calculate", key="sp"):
                try:

                    vsh = 1 - (psp / ssp)
                    if 0 < vsh < 1:
                        st.metric(
                            label="Shale Volume",
                            value=f"{vsh:.4g} | {vsh*100:.2f}%",
                        )
                    else:
                        st.error(
                            "The result cannot be superior to 100% nor negative. Please, check your values."
                        )

                except Exception as e:
                    st.warning("An error occurred: {e}")
        with tab2:
            st.write(
                "Another way to calculate the shale volume is by using this other equation:"
            )
            st.latex(r"V_{sh} = \frac{PSP - SSP}{SP_{shale} - SSP}")
            st.write(
                r"""Onde:  
                        $SP_{shale}$ - SP value on a shale (normally it's zero)"""
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
            if st.button("Calculate", key="sp_shale"):
                try:
                    # The result cannot be superior to 100% nor negative. Please, check your values.
                    vsh = (psp - ssp) / (sp_shale - ssp)
                    if 0 < vsh < 1:
                        st.metric(
                            label="Shale Volume",
                            value=f"{vsh:.4g} | {vsh*100:.2f}%",
                        )
                    else:
                        st.error(
                            "The result cannot be superior to 100% nor negative. Please, check your values."
                        )
                except Exception as e:
                    st.warning("An error occurred: {e}")

    with st.expander("Todas as equações"):

        igr = st.slider(r"$I_{GR} (decimal)$", min_value=0.0, max_value=1.0)

        try:
            fig = sv.plot_igr(igr_custom=igr)
            st.pyplot(fig)
        except ValueError as ve:
            st.warning(f"Erro: {ve}")
