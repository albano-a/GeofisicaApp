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

        st.write("##### Create a 1D NumPy array")
        values = [1, 2, 3, 4, 5]
        arr = np.array(values)
        st.code(
            f"""
values = [1, 2, 3, 4, 5]
arr = np.array(values)
# output: {arr}
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Create a 2D NumPy array")
        values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        arr = np.array(values)
        st.code(
            f"""
values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
arr = np.array(values)
# output: {arr}
            """,
            language="python",
            line_numbers=True,
        )

    with cols[1]:
        st.write("##### Check shape of array")
        values1 = [1, 2, 3, 4, 5]
        values2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        values3 = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        arr1 = np.array(values1)  # 1D
        arr2 = np.array(values2)  # 2D
        arr3 = np.array(values3)  # 3D

        shape1 = np.shape(arr1)
        shape2 = arr2.shape
        shape3 = arr3.shape
        st.code(
            f"""
values1 = [1, 2, 3, 4, 5]
values2 = [
    [1, 2, 3], 
    [4, 5, 6], 
    [7, 8, 9]
]
values3 = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
arr1 = np.array(values1) # 1D
arr2 = np.array(values2) # 2D
arr3 = np.array(values3) # 3D
# np.shape() or array.shape
shape1 = np.shape(arr1)     # output: {shape1}
shape2 = arr2.shape         # output: {shape2}
shape3 = arr3.shape         # output: {shape3}
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Create a 3x3 matrix")
        m = np.random.rand(3, 3)
        st.code(
            f"""
# random numbers between 0 and 1
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
        st.write("##### Element-wise operations")
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        st.code(
            f"""
# You can directly operate numpy arrays
add = a + b   # {a + b}
sub = a - b   # {a - b}
mul = a * b   # {a * b}
div = a / b   # {a / b}
            """,
            language="python",
            line_numbers=True,
        )
        
        
        
        st.write("##### Vector operations")
        
        st.code(
            f"""
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
# dot product
c1 = np.dot(a, b) # 1*4 + 2*5 + 3*6
c2 = a @ b
# cross product
c3 = np.cross(a, b)


print(c1) # output: {np.dot(a, b)}
print(c2) # output: {a @ b}
print(c3) # output: {np.cross(a, b)}
            """,
            language="python",
            line_numbers=True,
        )
