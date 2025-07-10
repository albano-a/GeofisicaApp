import streamlit as st
import math


def render_math():
    cols = st.columns(3)

    with cols[0]:
        st.write("Para importar a biblioteca")
        st.code(
            """
# To use any library in Python
# you first need to import it
import math         # without alias
import math as m    # with alias
            """,
            language="python",
            line_numbers=True,
        )
        st.write("Calculate seno, cosseno, e tangente:")
        st.code(
            f"""
# these angles are being calculated in radians
angle = 30
math.sin(angle) # {math.sin(30):.6f}...
math.cos(angle) # {math.cos(30):.6f}...
math.tan(angle) # {math.tan(30):.6f}...
            """,
            language="python",
            line_numbers=True,
        )
        st.write("Calculate arc sine, arc cosine, and arc tangent:")
        st.code(
            f"""
math.asin(0.5) # {math.asin(0.5):.6f}...
math.acos(0.5) # {math.acos(0.5):.6f}...
math.atan(0.5) # {math.atan(0.5):.6f}...
angle = 30
math.atan2(y, angle) 
# arc tangent of y/angle considering the quadrant
            """,
            language="python",
            line_numbers=True,
        )

    with cols[1]:
        st.write("Convert degrees to radians and vice versa:")
        st.code(
            f"""
angle_rad = math.radians(30)
# {math.radians(30)}
angle_deg = math.degrees(0.5)
# {math.degrees(0.5)}
            """,
            language="python",
            line_numbers=True,
        )

        st.write(r"Value of π, $\sqrt{}$ and $\log$:")
        st.code(
            f"""
math.pi # {math.pi}
math.sqrt(16) # {math.sqrt(16)}
math.log(100, 10) # {math.log(100, 10)}
            """,
            language="python",
            line_numbers=True,
        )

        st.write(r"Math constants")
        st.code(
            f"""
math.pi         # {math.pi}
math.e          # {math.e}
math.tau        # {math.tau}
math.inf        # {math.inf}
math.nan        # {math.nan}
            """,
            language="python",
            line_numbers=True,
        )

    with cols[2]:
        st.write("Rounding functions")
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

        st.write(r"Exponential and logarithmic functions")
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
        a, b, c = 3, 4, 5
        st.write(f"Number theory")
        st.code(
            f"""
a, b, c = 3, 4, 5
fat = math.factorial(c)
gcd = math.gcd(a, b, c)     # greatest common divisor
lcm = math.lcm(a, b, c)     # lowest common multiple
print(fat, gcd, lcm)
# output: 
# {math.factorial(c), math.gcd(a,b,c), math.lcm(a,b,c)}
            """
        )
