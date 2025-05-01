import streamlit as st
import random


def render_random():
    cols = st.columns(3)

    with cols[0]:
        st.write("#### Importar a biblioteca")
        st.code(
            """
            import random
            """,
            language="python",
            line_numbers=True,
        )
        st.write("##### Número aleatório inteiro entre a e b")
        st.code(
            """
            a = 1
            b = 10
            n = random.randint(a, b)
            print(n)
            """,
            language="python",
            line_numbers=True,
        )

    with cols[1]:
        st.write("##### Embaralhar elementos de uma lista")
        st.code(
            """
            l = [1, 2, 3, 4]
            random.shuffle(l)
            print(l)
            """,
            language="python",
            line_numbers=True,
        )

    with cols[2]:
        st.write("##### Escolher item aleatório de uma lista")
        st.code(
            """
            nomes = ["Ana", "João", "Carlos"]
            sorteado = random.choice(nomes)
            print(sorteado)
            """,
            language="python",
            line_numbers=True,
        )
