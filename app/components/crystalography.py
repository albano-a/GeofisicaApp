import plotly.graph_objects as go
import streamlit as st

"""
"Cubic",
"Tetragonal",
"Orthorhombic",
"Hexagonal",
"Triclinic",
"Monoclinic",
"Rhombohedral",
"""

def generate_crystal(tipo):
    if tipo == "Cubic":
        vertices = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1],
        ]
    elif tipo == "Tetragonal":
        vertices = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 2],
            [1, 0, 2],
            [1, 1, 2],
            [0, 1, 2],
        ]
    elif tipo == "Orthorhombic":
        vertices = [
            [0, 0, 0],
            [2, 0, 0],
            [2, 1, 0],
            [0, 1, 0],
            [0, 0, 3],
            [2, 0, 3],
            [2, 1, 3],
            [0, 1, 3],
        ]
    elif tipo == "Hexagonal":
        vertices = [
            [0, 0, 0],
            [1, 0, 0],
            [1.5, 0.866, 0],
            [0.5, 0.866, 0],
            [0, 0, 2],
            [1, 0, 2],
            [1.5, 0.866, 2],
            [0.5, 0.866, 2],
        ]
    elif tipo == "Triclinic":
        vertices = [
            [0, 0, 0],
            [1, 0.2, 0],
            [1.2, 1, 0],
            [0.2, 1, 0],
            [0, 0, 1.5],
            [1, 0.2, 1.5],
            [1.2, 1, 1.5],
            [0.2, 1, 1.5],
        ]
    elif tipo == "Monoclinic":
        vertices = [
            [0, 0, 0],
            [1, 0.2, 0],
            [1, 1.2, 0],
            [0, 1, 0],
            [0, 0, 2],
            [1, 0.2, 2],
            [1, 1.2, 2],
            [0, 1, 2],
        ]
    elif tipo == "Rhombohedral":
        vertices = [
            [0, 0, 0],
            [1, 0.2, 0],
            [1.2, 1, 0],
            [0.2, 1, 0],
            [0, 0, 1],
            [1, 0.2, 1],
            [1.2, 1, 1],
            [0.2, 1, 1],
        ]
    else:
        # Valor inválido para tipo
        st.error(f"Crystal system '{tipo}' not recognized.")
        return go.Figure()  # Retorna um gráfico vazio

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]

    fig = go.Figure()

    for edge in edges:
        x = [vertices[edge[0]][0], vertices[edge[1]][0]]
        y = [vertices[edge[0]][1], vertices[edge[1]][1]]
        z = [vertices[edge[0]][2], vertices[edge[1]][2]]
        fig.add_trace(
            go.Scatter3d(
                x=x, y=y, z=z, mode="lines", line=dict(color="#bc1077", width=6)
            )
        )

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=2.5)),
        ),
        width=350,
        height=350,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False,
    )
    return fig
