import numpy as np
import matplotlib.pyplot as plt


def larionov(igr):
    return 0.083 * (2 ** (3.7 * igr) - 1)


def larionov_old_rocks(igr):
    return 0.33 * (2 ** (2 * igr) - 1)


def steiber(igr):
    return igr / (3 - 2 * igr)


def clavier(igr):
    return 1.7 - (3.38 - (igr + 0.7) ** 2) ** (1 / 2)


def plot_igr(igr_custom=None):
    if igr_custom is None:
        raise ValueError("Please provide a valid value for 'igr_custom'.")

    if not (0 <= igr_custom <= 1):
        raise ValueError("'igr_custom' must be between 0 and 1.")

    igr = np.linspace(0, 1, 100)

    vsh_larionov = larionov(igr)
    vsh_larionov_or = larionov_old_rocks(igr)
    vsh_steiber = steiber(igr)
    vsh_clavier = clavier(igr)

    vsh_lar_custom = larionov(igr_custom)
    vsh_lar_or_custom = larionov_old_rocks(igr_custom)
    vsh_steiber_custom = steiber(igr_custom)
    vsh_clavier_custom = clavier(igr_custom)

    labels = {
        "Larionov": f"Larionov - {vsh_lar_custom * 100:.2f}%",
        "Larionov Old Rocks": f"Larionov Old Rocks - {vsh_lar_or_custom * 100:.2f}%",
        "Steiber": f"Steiber - {vsh_steiber_custom * 100:.2f}%",
        "Clavier": f"Clavier - {vsh_clavier_custom * 100:.2f}%",
        "IGR": f"IGR - {igr_custom*100:.2f}%",
    }

    fig, axs = plt.subplots(1, 1, figsize=(8, 6))

    axs.plot(igr, igr, "--", color="black", label=r"$I_{GR} Linear$")
    axs.plot(igr, vsh_larionov_or, color="#c00000", label=labels["Larionov Old Rocks"])
    axs.plot(igr, vsh_clavier, color="#006500", label=labels["Clavier"])
    axs.plot(igr, vsh_steiber, color="#ff00ff", label=labels["Steiber"])
    axs.plot(igr, vsh_larionov, color="#0000ff", label=labels["Larionov"])
    axs.axvline(igr_custom, color="gray", linestyle="--", label=labels["IGR"])

    axs.set_title(r"$V_{shale}$ as a function of $I_{GR}$")
    axs.set_xlabel(r"$I_{GR}$: Gamma Ray Index")
    axs.set_ylabel(r"$V_{sh} = f(I_{GR})$")
    axs.legend(loc="best")

    axs.grid(True)

    return fig
