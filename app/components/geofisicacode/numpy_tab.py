import streamlit as st
import numpy as np

def render_numpy():
    cols = st.columns(3)
    
    with cols[0]:
        st.write("##### Criar array NumPy e somar todos os elementos")
        st.code(
            """
            import numpy as np
            arr = np.array([1, 2, 3, 4])
            print(np.sum(arr))
            """,
            language="python",
            line_numbers=True,
        )

        
        
        
    with cols[1]:
        st.write("##### Criar matriz 3x3 com números aleatórios")
        st.code(
            """
            import numpy as np
            m = np.random.rand(3, 3)
            print(m)
            """,
            language="python",
            line_numbers=True,
        )
        
        
        
    with cols[2]:
        st.write("##### Operações vetoriais com NumPy")
        st.code(
            """
            import numpy as np
            a = np.array([1, 2, 3])
            b = np.array([4, 5, 6])
            c = a + b
            print(c)
            """,
            language="python",
            line_numbers=True,
        )
        
        
        