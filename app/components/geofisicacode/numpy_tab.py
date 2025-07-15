import streamlit as st
import numpy as np


def render_numpy():
    st.write(
        """
        NumPy is widely used in scientific computing, data analysis, machine learning, and engineering due to its speed and versatility.
        """
    )

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

        st.write("##### Creating an array of zeros or ones")
        zeros = np.zeros(3)
        ones = np.ones((3, 3))
        st.code(
            f"""
zeros = np.zeros(3)
ones = np.ones((3,3))
print(zeros) # a 1D array with 3 elements
# output
{zeros}
print(ones) # a 2D array with 9 elements
# output
{ones}
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Flattening an array")
        M = np.array([[12, 7, 26], [32, 10, 1]])
        st.code(
            f"""
M = np.array([
    [12, 7, 26],
    [32, 10, 1]
])
M.flatten()
# output
{M.flatten()}
            """
        )

        st.write("##### Selecting unique values")
        a = np.array([1, 2, 3, 4, 5, 2, 4])
        b = np.array([12, 13, 14, 12, 15, 11, 13])
        u_val = np.unique(a)
        st.code(
            f"""
a = np.array([1, 2, 3, 4, 5, 2, 4])
u_val = np.unique(a)
# output
{u_val}
            """
        )

        st.write("##### Concatenating arrays along an axis")
        conc = np.concatenate([a, b], axis=0)
        st.code(
            f"""
b = np.array([12, 13, 14, 12, 15, 11, 13])
conc = np.concatenate([a, b], axis=0)
{conc}
            """
        )

    with cols[1]:
        st.write("##### Check shape of array")
        values1 = [1, 2, 3, 4, 5, 6]
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
values1 = [1, 2, 3, 4, 5, 6]
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
shape1 = np.shape(arr1)  # output: {shape1}
shape2 = arr2.shape      # output: {shape2}
shape3 = arr3.shape      # output: {shape3}""",
            language="python",
            line_numbers=True,
        )

        st.write("##### Reshape an array")
        arr1 = arr1.reshape(3, 2)
        st.code(
            f"""
arr1 = np.array([1, 2, 3, 4, 5, 6])
arr1.reshape(3, 2)
print(arr1)
# output
{arr1}"""
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
'''""",
            language="python",
            line_numbers=True,
        )

        st.write("##### Statistic using NumPy")
        matrix = np.array([[9.8, 7.9, 8.8], [6.2, 6.8, 7.4], [8.5, 9.2, 8.7]])
        s = np.sum(matrix)
        mean = np.mean(matrix)
        std = np.std(matrix)
        max = np.max(matrix)
        min = np.min(matrix)

        st.code(
            f"""
matrix = np.array([
    [9.8, 7.9, 8.8],
    [6.2, 6.8, 7.4],
    [8.5, 9.2, 8.7]
])
s = np.sum(matrix)      # {s}
mean = np.mean(matrix)  # {mean}
std = np.std(matrix)    # {std}
max = np.max(matrix)    # {max}
min = np.min(matrix)    # {min}"""
        )

        st.write("##### Vertically or Horizontally stacking arrays")
        vstack = np.vstack([a, b])
        hstack = np.hstack([a, b])

        st.code(
            f"""
vstack = np.vstack([a, b])
hstack = np.hstack([a, b])
# vstack
{vstack}
# hstack
{hstack}
            """
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
div = a / b   # {a / b}""",
            language="python",
            line_numbers=True,
        )

        st.write("##### Generate arrays with `linspace` and `arange`")
        cols = st.columns(3)
        with cols[0]:
            start = st.number_input("Start", step=1, value=0)
        with cols[1]:
            stop = st.number_input("Stop", step=1, value=10)
        with cols[2]:
            step = st.number_input("Step", min_value=1, value=5)
        array1 = np.arange(start, stop, step)
        array2 = np.linspace(1, 10, step)
        st.code(
            f"""
array1 = np.arange({start}, {stop}, {step})
array2 = np.linspace({start}, {stop}, {step})
print(array1) # {array1} 1, 1 + {step}...
print(array2) # {array2}"""
        )
        st.write(
            """
            `arange` - spacing defined by step size  
            `linspace` - spacing defined by number of elements (not step)
            """
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
print(c3) # output: {np.cross(a, b)}""",
            language="python",
            line_numbers=True,
        )

        st.write("##### Transposing a matrix")
        A = np.array([[1, 2], [4, 9]])
        st.code(
            f"""
A = np.array([
    [1, 2],
    [4, 9]
])
print(A.T)
# ouput
{A.T}
            """
        )

        st.write("##### Using `where`")
        a = np.array([[-5, 1, -2], [3, 4, -1], [5, -1, -2]])

        st.write("Write a condition using `a`. Example: `a < 0`, `a % 2 == 0`, `a > 2`")
        cols = st.columns(3)
        with cols[0]:
            cond = st.text_input("Condition", value="a < 0")
        with cols[1]:
            x = st.number_input("Value if True", value=0)
        with cols[2]:
            y = st.number_input("Value if False", value=1)
        mask = eval(cond, {"a": a, "np": np})
        result = np.where(mask, x, y)
        st.code(
            f"""
a = np.array([
    [-5, 1, -2], 
    [3, 4, -1], 
    [5, -1, -2]
])
where = np.where({cond}, {x}, {y})  # conditional
# output
{result}
            """
        )
