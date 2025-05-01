import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy
import components.sidebar as sidebar

st.set_page_config(
    page_title="GeofisicaCode",
    page_icon="assets/geofisicacode_favicons.svg",
    layout="wide",
)

sidebar.show()

st.image("assets/GeofisicaCode.svg", width=600, output_format="PNG")

cols = st.columns(3)

with cols[0]:
    st.write("Para imprimir algo na tela, use:")
    st.code(
        """
        print("Hello World")
        """,
        language="python",
        line_numbers=True,
    )
    st.write("Para iterar por duas listas ao mesmo tempo")
    st.code(
        """
        for nome, nota in zip(nomes, notas):
            print(f"{nome}: {nota}")
        """,
        language="python",
        line_numbers=True,
    )

with cols[1]:
    st.write("Para inverter strings")
    st.code(
        """
        texto = "Olá, Python"
        print(texto[::-1])
        """,
        language="python",
        line_numbers=True,
    )

    st.write("Acessar índice e valor ao mesmo tempo")
    st.code(
        """
        for i, val in enumerate(lista):
            print(i, val)
        """,
        language="python",
        line_numbers=True,
    )

with cols[2]:
    st.write("Troca de valores entre variáveis, sem variável temporária")
    a = 3
    b = 4
    st.code(
        f"""
        a = {a}
        b = {b} 
        a, b = b, a
        # a = {b}
        # b = {a}
        """,
        language="python",
        line_numbers=True,
    )

    st.write("Criar listas de forma compacta")
    quadrados = [xx**2 for xx in range(10)]
    st.code(
        f"""
        quadrados = [x**2 for x in range(10)]
        # {quadrados}
        """,
        language="python",
        line_numbers=True,
    )

st.divider()
st.subheader("Bibliotecas - Math")

cols = st.columns(3)

with cols[0]:
    st.write("Para importar a biblioteca")
    st.code(
        """
        import math
        """,
        language="python",
        line_numbers=True,
    )
    st.write("Calcular seno, cosseno, e tangente:")
    st.code(
        f"""
        angle = 30
        math.sin(angle) # {math.sin(30):.6f}...
        math.cos(angle) # {math.cos(30):.6f}...
        math.tan(angle) # {math.tan(30):.6f}...
        """,
        language="python",
        line_numbers=True,
    )
    st.write("Calcular arco seno, arco cosseno, e arco tangente:")
    st.code(
        f"""
        angle = 30
        math.asin(angle) # {math.asin(0.5)}
        math.acos(angle) # {math.acos(0.5)}
        math.atan(angle) # {math.atan(0.5)}
        math.atan2(y, angle) # arco tangente de y/angle considerando quadrante
        """,
        language="python",
        line_numbers=True,
    )

with cols[1]:
    st.write("Converter graus para radianos e vice-versa:")
    st.code(
        f"""
        angle_deg = 30
        angle_rad = math.radians(angle_deg)
        # {math.radians(30)}
        angle_rad = 0.5
        angle_deg = math.degrees(angle_rad_2)
        # {math.degrees(0.5)}
        """,
        language="python",
        line_numbers=True,
    )

    st.write(r"Valor de π, $\sqrt{}$ e $\log$:")
    st.code(
        f"""
        math.pi # {math.pi}
        math.sqrt(16) # {math.sqrt(16)}
        math.log(100, 10) # {math.log(100, 10)}
        """,
        language="python",
        line_numbers=True,
    )

with cols[2]:
    st.write("Funções de arredondamento")
    n1 = 5.2
    st.code(
        f"""
        n1 = {n1}
        math.ceil(n1) # {math.ceil(n1)}
        math.floor(n1) # {math.floor(n1)}
        math.trunc(n1) # {math.trunc(n1)}
        """,
        language="python",
        line_numbers=True,
    )

    st.write(r"Funções exponenciais e logarítmicas")
    n2 = 4
    st.code(
        f"""
        n2 = {n2}
        math.exp(x) # {math.exp(n2)}
        math.log(x) # {math.log(n2)}
        math.log(x, base) # {math.log(n2, 3)}
        math.log10(x) # {math.log10(n2)}
        math.log2(x) # {math.log2(n2)}
        """,
        language="python",
        line_numbers=True,
    )
