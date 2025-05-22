import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def render_matplotlib():
    cols = st.columns(3)

    with cols[0]:
        st.write("##### Importação")
        st.code(
            """
            import matplotlib.pyplot as plt
            """,
            language="python",
            line_numbers=True,
        )
        st.write("##### Criar gráfico de linha simples")
        st.code(
            """
            x = [1, 2, 3]
            y = [2, 4, 1]
            plt.plot(x, y)
            plt.show()
            """,
            language="python",
            line_numbers=True,
        )
        x = [1, 2, 3]
        y = [2, 4, 1]
        fig, ax = plt.subplots(1, 1)
        ax.plot(x, y)
        st.pyplot(fig)

    with cols[1]:
        st.write("##### Bar Plot")
        st.code(
            """
            names = ["A", "B", "C"]
            values = [10, 20, 15]
            plt.bar(names, values)
            plt.show()
            """,
            language="python",
            line_numbers=True,
        )
        nomes = ["A", "B", "C"]
        valores = [10, 20, 15]
        fig, ax = plt.subplots(1, 1)
        ax.bar(nomes, valores)
        st.pyplot(fig)

        st.write("##### Histograma")
        st.code(
            """
            data = np.random.randn(1000)
            plt.hist(data, bins=30)
            plt.show()
            """
        )
        bins = st.slider("Bins", min_value=1, max_value=100)
        data = np.random.randn(1000)
        fig, ax = plt.subplots(1, 1)
        ax.hist(data, bins=bins, edgecolor="black")
        st.pyplot(fig)

    with cols[2]:
        st.write("##### Gráfico de dispersão (scatter)")
        st.code(
            """
            import numpy as np
            x = np.random.rand(50)
            y = np.random.rand(50)
            plt.scatter(x, y)
            plt.show()
            """,
            language="python",
            line_numbers=True,
        )

        x = np.random.rand(50)
        y = np.random.rand(50)
        fig, ax = plt.subplots(1, 1)
        ax.scatter(x, y)
        st.pyplot(fig)
