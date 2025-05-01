from streamlit.testing.v1 import AppTest
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)  # adiciona a raiz do projeto ao PYTHONPATH


def test_resistivity_apparent():
    at = AppTest.from_file(
        "app/pages/PetrofisicaHub.py", default_timeout=10
    )  # Testa diretamente essa página
    at.run()

    assert len(at.tabs) >= 3
    tab = at.tabs[2]
    tab.select()

    tab.radio[0].set_value(r"Resistividade Aparente - $R_{wa}$")
    tab.number_input["resist_input_rt"].set_value(2.0)
    tab.number_input["expoente_cimentacao_1"].set_value(2.0)
    tab.number_input["resist_phi"].set_value(0.25)
    tab.number_input["fator_tortuosidade_1"].set_value(1.0)

    tab.button("Calculate", key=4).click()

    assert tab.metric[0].label == "Resistividade Aparente da Água"
    assert tab.metric[0].value == "0.1250 ohm-m"
