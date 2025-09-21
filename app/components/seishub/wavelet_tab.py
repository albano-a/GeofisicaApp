import streamlit as st
import numpy as np
import io
import matplotlib.pyplot as plt
from helpers.img_export import export_as_svg
from components.seishub.functions.wavelets import ricker, butterworth
import pandas as pd


def render_wavelet():
    st.write(
        "Wavelets are short-duration oscillatory signals used to represent and analyze seismic waves. They are fundamental to how seismic data is generated, interpreted, and processed."
    )

    _wavelets = ["Ricker", "Butterworth"]

    wavelet = st.tabs(_wavelets)

    with wavelet[0]:
        st.write(
            """
            Ricker wavelets are zero-phase wavelets with a central peak and two smaller side lobes. A Ricker wavelet
            can be uniquely specified with only a single parameter, `f`, it's peak frequency. The formula for a Ricker
            wavelet is given by (Ryan, H - Ricker, Ormsby, Klauder, Butterworth - A Choice of Wavelets):
            """
        )
        st.latex(r"(1 - 2\pi^{2}f^{2}t^{2})e^{(-\pi^{2}f^{2}t^{2})}")
        st.markdown("---")

        st.write(
            "Generate the Ricker wavelet using the inputs below. You can export the image or the data, for future use on geophysics software."
        )
        cols = st.columns(3)

        with cols[0]:
            peak_freq = st.number_input("Peak Frequency", min_value=0.00, value=15.00)
        with cols[1]:
            dt = st.number_input(
                "Time (ms)",
                min_value=0.00,
                value=4.00,
                help="Normally, this value is either 2 or 4 ms",
            )
        with cols[2]:
            samples_ricker = st.number_input("Samples", min_value=0, value=100)

        with st.expander("Calculate and Plot"):
            try:
                t, rwv, freqs, fft = ricker(peak_freq, dt=dt, samples=samples_ricker)

                csv = (
                    pd.DataFrame({"time": t, "amplitude": rwv})
                    .to_csv(index=False, sep=",")
                    .encode("utf-8")
                )
                st.download_button(
                    label="Export data",
                    data=csv,
                    file_name=f"ricker_{peak_freq}.txt",
                    mime="text/plain",
                    width="stretch",
                )

                tabs = st.tabs(["Time", "Frequency"])

                with tabs[0]:
                    # Improved horizontal alignment for controls
                    col1, col5, col2, col3, col4 = st.columns([2, 1, 0.5, 0.75, 0.75])
                    with col1:
                        title = st.text_input("Title", value="Ricker - Time")
                    with col2:
                        color_t = st.color_picker("Color", value="#3389bc", key="time")
                    with col3:
                        leg = st.checkbox("Legend?", value=True)
                    with col4:
                        gridd = st.checkbox("Grid?", value=True)
                    with col5:
                        themes = st.selectbox(
                            "Theme",
                            options=["default", "bmh", "ggplot", "seaborn-v0_8"],
                            key="ricker_theme",
                        )
                    plt.style.use([themes])

                    fig, axs = plt.subplots()
                    axs.plot(t, rwv, color=color_t, label="Ricker")
                    axs.set_ylabel("Amplitude")
                    axs.set_xlabel("Time (ms)")
                    if leg:
                        axs.legend(loc="upper right")
                    if gridd and themes == "default":
                        axs.grid(
                            True,
                            which="major",
                            linestyle="--",
                            linewidth=0.5,
                            alpha=0.7,
                        )
                        axs.grid(
                            True, which="minor", linestyle=":", linewidth=0.3, alpha=0.5
                        )
                        axs.minorticks_on()
                    axs.set_title(title)

                    st.pyplot(fig)
                    export_as_svg(fig, fname="Ricker_time")

                with tabs[1]:
                    # Improved horizontal alignment for controls
                    col1, col5, col2, col3, col4 = st.columns([2, 1, 0.5, 0.75, 0.75])
                    with col1:
                        title = st.text_input("Title", value="Ricker - Frequency")
                    with col2:
                        color_f = st.color_picker(
                            "Color", value="#3389bc", key="ricker_freq_color"
                        )
                    with col3:
                        leg = st.checkbox("Legend?", value=True, key="ricker_freq_leg")
                    with col4:
                        gridd = st.checkbox("Grid?", value=True, key="ricker_freq_grid")
                    with col5:
                        themes = st.selectbox(
                            "Theme",
                            options=["default", "bmh", "ggplot", "seaborn-v0_8"],
                            key="ricker_freq_theme",
                        )
                    plt.style.use([themes])

                    fig, axs = plt.subplots()
                    axs.plot(freqs, fft, color=color_f, label="Frequency")
                    axs.set_ylabel("Amplitude")
                    axs.set_xlabel("Frequency (Hz)")
                    if leg:
                        axs.legend(loc="upper right")
                    if gridd and themes == "default":
                        axs.grid(
                            True,
                            which="major",
                            linestyle="--",
                            linewidth=0.5,
                            alpha=0.7,
                        )
                        axs.grid(
                            True, which="minor", linestyle=":", linewidth=0.3, alpha=0.5
                        )
                        axs.minorticks_on()
                    axs.set_title(title)

                    st.pyplot(fig)
                    export_as_svg(fig, fname="Ricker_freq")

            except Exception as e:
                st.error(f"An error occurred: {e}")

    with wavelet[1]:
        st.markdown(
            """
            <div style="text-align: justify;">
            The Butterworth wavelet is a minimum-phase, physically realizable wavelet that begins at time zero, distinguishing it from zero-phase wavelets like Ricker or Ormsby. Derived from the Butterworth filter, which is characterized by maximal flatness in the passband, this wavelet is defined by four key parameters: the lower (<code>fl</code>) and upper (<code>fh</code>) frequencies of the bandpass, and the cutoff rates, described either by filter order (<code>n</code>) or in decibels per octave (<code>6n</code>). As the cutoff rate increases, the resulting wavelet becomes more extended or "leggy." Its construction is mathematically rigorous, and tools like MATLAB simplify its generation via built-in Butterworth filter functions.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown(
            "Generate the Butterworth wavelet below using the inputs. You can export the data for use in geophysics software."
        )
        cols = st.columns(4)
        with cols[0]:
            h_f = st.number_input("High Frequency", min_value=0.00, value=60.0)
        with cols[1]:
            l_f = st.number_input("Low Frequency", min_value=0.00, value=10.0)
        with cols[2]:
            dt = st.number_input(
                "Time (ms)",
                min_value=0.00,
                value=4.00,
                help="Normally, this value is either 2 or 4 ms",
                key="butterworth_dt",
            )
        with cols[3]:
            samples = st.number_input(
                "Samples", min_value=0, value=36, key="butterworth_samples"
            )

        with st.expander("Calculate and Plot"):
            try:
                t, bwv, freqs, fft = butterworth(h_f, l_f, samples=samples, dt=dt)

                csv = (
                    pd.DataFrame({"time": t, "amplitude": bwv})
                    .to_csv(index=False, sep=",")
                    .encode("utf-8")
                )
                st.download_button(
                    label="Export data",
                    data=csv,
                    file_name=f"butter_{peak_freq}.txt",
                    mime="text/plain",
                    width="stretch",
                )

                tabs = st.tabs(["Time", "Frequency"])

                with tabs[0]:
                    cols = st.columns(2)
                    with cols[0]:
                        title = st.text_input("Change title", value="Butter - Time")
                    with cols[1]:
                        color_t = st.color_picker(
                            "Plot color", value="#3389bc", key="butter-time"
                        )
                    fig, axs = plt.subplots(1, 1)
                    axs.plot(t, bwv, color=color_t, label="Butter")
                    axs.set_ylabel("Amplitude")
                    axs.set_xlabel("Time (ms)")
                    leg = st.checkbox("Show legend", key="butter-1-legend")
                    if leg == True:
                        axs.legend(loc="upper right")

                    axs.set_title(title)

                    st.pyplot(fig)

                    export_as_svg(fig, fname="Butter_time")

                with tabs[1]:
                    cols = st.columns(2)
                    with cols[0]:
                        title = st.text_input(
                            "Change title",
                            value="Butter - Frequency",
                            key="butter-freq1",
                        )
                    with cols[1]:
                        color_t = st.color_picker(
                            "Plot color", value="#3389bc", key="butter-freq2"
                        )
                    fig, axs = plt.subplots(1, 1)
                    axs.plot(freqs, fft, color=color_t)
                    axs.set_ylabel("Amplitude")
                    axs.set_xlabel("Frequency (Hz)")
                    leg = st.checkbox("Show legend", key="butter-2-legend")
                    if leg == True:
                        axs.legend(loc="upper right")

                    axs.set_title(title)

                    st.pyplot(fig)

                    export_as_svg(fig, fname="Butter_freq")

            except Exception as e:
                st.error(f"An error occurred: {e}")
