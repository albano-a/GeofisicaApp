import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from helpers.img_export import export_as_svg


def render_matplotlib():
    cols = st.columns(3)

    with cols[0]:
        st.write("##### Import module")
        st.code(
            """
# Most used alias
import matplotlib.pyplot as plt""",
            language="python",
            line_numbers=True,
        )
        st.write("##### Simple plot")
        subcols = st.columns(2)
        with subcols[0]:
            x = st.text_input("Enter list 1", value="1, 2, 3").split(",")
            x = [int(i) for i in x]
        with subcols[1]:
            y = st.text_input("Enter list 2", value="3, 4, 5").split(",")
            y = [int(j) for j in y]

        if not x or not y:
            st.warning("Both lists must have at least one number.")
        elif len(x) != len(y):
            st.warning("Lists must be the same length.")
        else:
            st.code(
                f"""
x = {x}
y = {y}
plt.plot(x, y)
plt.show()""",
                language="python",
                line_numbers=True,
            )

            fig, ax = plt.subplots()
            ax.plot(x, y)
            st.pyplot(fig)
        st.write("##### Heatmap")
        st.code(
            """
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(50, 50)
plt.imshow(data, cmap='viridis', aspect='auto')
plt.colorbar()
plt.show()
            """
        )
        cmap = st.selectbox("Colormap", ["viridis", "gray", "rainbow", "RdBu"])
        data = np.random.rand(50, 50)
        fig, ax = plt.subplots(1, 1)
        ax.imshow(data, cmap=cmap, aspect="auto")
        st.pyplot(fig)

        st.write("Styling")
        subcols2 = st.columns(2)
        with subcols2[0]:
            color = st.text_input("Color (red, C4, #00ff00)", value="#0000ff")
        with subcols2[1]:
            grid = st.checkbox("Grid", value=True)

        st.code(
            rf"""
import numpy as np

x = np.linspace(-1, 1, 100)
y = np.sin(x)

fig, axs = plt.subplots(1, 1)
axs.plot(x, y, color="{color}")
axs.set_title("Sine of X", fontsize=18)
axs.set_ylabel(r"$\sin(x)$")
axs.set_xlabel("Values of X", fontsize=14)

axs.grid({grid}, which="major", linestyle="--", linewidth=0.5, alpha=0.7)
axs.grid({grid}, which="minor", linestyle=":", linewidth=0.3, alpha=0.5)
axs.minorticks_on()

plt.tight_layout()
plt.show()
            """
        )
        x = np.linspace(-1, 1, 100)
        y = np.sin(x)

        fig, axs = plt.subplots(1, 1)
        axs.plot(x, y, color=color)
        axs.set_title("Sine of X", fontsize=18)
        axs.set_ylabel(r"$\sin(x)$")
        axs.set_xlabel("Values of X", fontsize=14)

        if grid == True:
            axs.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.7)
            axs.grid(True, which="minor", linestyle=":", linewidth=0.3, alpha=0.5)

        axs.minorticks_on()

        plt.tight_layout()
        st.pyplot(fig)
        export_as_svg(fig, "Plot example", fformat="png")

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

        st.write("##### Histogram")
        st.code(
            """
data = np.random.randn(1000)
plt.hist(data, bins=30)
plt.show()
            """
        )
        bins = st.slider("Bins", min_value=1, value=30, max_value=100)
        data = np.random.randn(1000)
        fig, ax = plt.subplots(1, 1)
        ax.hist(data, bins=bins, edgecolor="black")
        st.pyplot(fig)

        st.write("##### 3D plot")
        st.code(
            """
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

ax.plot_surface(X, Y, Z, cmap='coolwarm')
plt.show()
            """
        )
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))

        ax.plot_surface(X, Y, Z, cmap="viridis")

        st.pyplot(fig)

    with cols[2]:
        st.write("##### Scatter plot")
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

        st.write("##### Pizza plot")
        cols = st.columns(2)
        sizeA = cols[0].slider("Size A", 0, 100, 30)
        sizeB = cols[1].slider("Size B", 0, 100 - sizeA, 20)
        sizeC = 100 - sizeA - sizeB
        st.code(
            f"""
sizes = [{sizeA}, {sizeB}, {sizeC}]
labels = ['A', 'B', 'C']

plt.pie(sizes, labels=labels)
plt.show()
            """
        )
        sizes = [sizeA, sizeB, sizeC]
        labels = ["A", "B", "C"]
        fig, ax = plt.subplots(1, 1)

        ax.pie(sizes, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)

        st.write("##### Different styles")
        styles = st.selectbox(
            "Choose style",
            options=[
                "default",
                "classic",
                "bmh",
                "Solarize_Light2",
                "dark_background",
                "fast",
                "fivethirtyeight",
                "ggplot",
                "grayscale",
                "petroff10",
                "seaborn-v0_8",
            ],
        )
        with plt.style.context([styles]):
            st.code(
                """
import numpy as np
x = np.linspace(-5, 5, 100)
y = np.sin(x)
z = np.cos(x)

with plt.style.context(['bmh']):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.plot(x, z)
    plt.show()""",
                language="python",
            )
            x = np.linspace(-5, 5, 100)
            y = np.sin(x)
            z = np.cos(x)
            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.plot(x, z)
            st.pyplot(fig)
