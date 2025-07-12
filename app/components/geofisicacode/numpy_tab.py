import streamlit as st
import numpy as np


def render_numpy():
    cols = st.columns(3)

    with cols[0]:
        st.write("##### Import module")
        st.code(
            """
# To import any module in python, we use
import numpy           # without alias
import numpy as np     # with alias (more common)
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Create a NumPy array and sum all elements")
        arr = np.array([1, 2, 3, 4, 5])
        summ = np.sum(arr)
        st.code(
            f"""
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(np.sum(arr))
# output: {summ}
            """,
            language="python",
            line_numbers=True,
        )

    with cols[1]:
        st.write("##### Create a 3x3 matrix with random numbers between 0 and 1")
        m = np.random.rand(3, 3)
        st.code(
            f"""
m = np.random.rand(3, 3)
print(m)
'''
output:
{m}
'''
            """,
            language="python",
            line_numbers=True,
        )

    with cols[2]:
        st.write("##### Vector operations with NumPy")
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        st.code(
            f"""
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.dot(a, b) # 1*4 + 2*5 + 3*6
print(c)
# output: {np.dot(a, b)}
            """,
            language="python",
            line_numbers=True,
        )
