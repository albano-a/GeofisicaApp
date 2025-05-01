import streamlit as st
import pandas as pd


def render_pandas():
    cols = st.columns(3)

    with cols[0]:
        st.write("Importação")
        st.code("import pandas as pd", language='python', line_numbers=True)
        st.write("##### Criar DataFrame a partir de dicionário")
        st.code(
            """
            import pandas as pd
            dados = {"Nome": ["Ana", "João"], "Idade": [23, 30]}
            df = pd.DataFrame(dados)
            print(df)
            """,
            language="python",
            line_numbers=True,
        )

    with cols[1]:
        st.write("##### Ler CSV e mostrar as 5 primeiras linhas")
        st.code(
            """
            import pandas as pd
            df = pd.read_csv("dados.csv")
            print(df.head())
            """,
            language="python",
            line_numbers=True,
        )

    with cols[2]:
        st.write("##### Filtrar linhas por condição")
        st.code(
            """
            import pandas as pd
            df = pd.DataFrame(
                {
                    "Nome": ["Ana", "João"], 
                    "Idade": [23, 30]
                }
            )
            adultos = df[df["Idade"] >= 25]
            print(adultos)
            """,
            language="python",
            line_numbers=True,
        )
