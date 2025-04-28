import numpy as np
import streamlit as st
import stoneforge


def correct_petrophysic_estimation_range(petrophysics_data):
    if np.isscalar(petrophysics_data):
        if petrophysics_data > 1:
            petrophysics_data = 1
        elif petrophysics_data < 0:
            petrophysics_data = 0
    else:
        petrophysics_data[petrophysics_data > 1] = 1
        petrophysics_data[petrophysics_data < 0] = 0

    return petrophysics_data


def effective_porosity(phi, vsh):
    phie = phi - vsh
    phie = correct_petrophysic_estimation_range(phie)
    return phie


def density_porosity(rhob, rhom, rhof):
    """Estimate the porosity from the bulk density log"""
    # Verificar se rhob é um array ou um valor escalar
    is_array = isinstance(rhob, (np.ndarray, list))

    if rhom == rhof:
        st.warning("This will result in a division by zero.", icon="🚨")
        return np.nan  # Retorna NaN para evitar divisão por zero

    if (
        rhom < rhof
        or (is_array and any(rhom <= rhob))
        or (not is_array and rhom <= rhob)
    ):
        st.warning("Rho_Matriz must be greater than Rho_fluid and Rho_Log", icon="🚨")
        # return np.nan  # Retorna NaN para valores inválidos

    if is_array and any(rhom - rhob > rhom - rhof):
        st.warning("rhob value is lower than rhof", icon="🚨")
        # return np.nan  # Retorna NaN para valores inválidos

    # Cálculo da porosidade
    phi = (rhom - rhob) / (rhom - rhof)

    # Corrigir valores fora do intervalo [0, 1]
    # phi = correct_petrophysic_estimation_range(phi)
    return phi


def neutron_porosity(nphi: np.ndarray, vsh: np.ndarray, nphi_sh: float):
    return stoneforge.petrophysics.porosity.neutron_porosity(
        nphi=nphi, vsh=vsh, nphi_sh=nphi_sh
    )


def neutron_density_porosity(
    phid: np.ndarray, phin: np.ndarray, squared: bool = False
) -> np.ndarray:
    """Estimate the effective porosity by calculating the mean of Bulk Density porosity and Neutron porosity"""
    if squared == False:
        if np.any((phid + phin / 2) > 1):
            st.warning("The value must be a value between 0 and 1")

            phi = (phid + phin) / 2
        else:
            phi = (phid + phin) / 2

    elif squared == True:
        if np.any((phid**2 + phin**2 / 2) > 1):
            st.warning("The value must be a value between 0 and 1")

            phi = np.sqrt((phid**2 + phin**2) / 2)

        else:
            phi = np.sqrt((phid**2 + phin**2) / 2)

    # phi = correct_petrophysic_estimation_range(phi)
    return phi


def sonic_porosity(dt: np.ndarray, dtma: float, dtf: float):
    """Estimate the Porosity from sonic using the Wyllie time-average equation [1]_."""
    if dtf == dtma:
        st.warning("This will result in a division by zero")

        return np.nan

    else:
        if np.any(dt <= dtma) or dtf <= dtma:
            st.warning("dt and dtf must be greater than dtma")

            phidt = (dt - dtma) / (dtf - dtma)

        elif np.any(dt - dtma > dtf - dtma):
            st.warning("dt value is greather than dtf")

            phidt = (dt - dtma) / (dtf - dtma)

        else:
            phidt = (dt - dtma) / (dtf - dtma)

    #phidt = correct_petrophysic_estimation_range(phidt)
    return phidt


def gaymard_porosity(phid, phin):
    """Estimate the effective porosity using Gaymard-Poupon [1]_ method."""
    phie = (0.5 * (phid * phid + phin * phin)) ** 0.5

    #phie = correct_petrophysic_estimation_range(phie)
    return phie
