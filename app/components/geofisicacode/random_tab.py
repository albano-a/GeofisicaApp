import streamlit as st  # type: ignore
import random


def render_codeblock(title, code):
    st.write(f"##### {title}")
    st.code(
        code,
        language="python",
        line_numbers=True,
    )


def render_random():
    cols = st.columns(3)

    with cols[0]:
        render_codeblock(
            title="Import module",
            code="""
# To import any module in python, we use
import random           # without alias
import random as rd     # with alias
""",
        )
        render_codeblock(
            title="Random float between 0 and 1",
            code="""
x = random.random()
print(x)  # example: 0.374
            """,
        )

        render_codeblock(
            title="Random float: 2.5 <= x < 10",
            code="""
x = random.uniform(2.5, 10.0)
print(x) # example: 3.1800146073117523
            """,
        )

        render_codeblock(
            title="Interval between arrivals averaging 5 seconds",
            code="""
x = random.expovariate(1 / 5)
print(x) # example: 5.148957571865031
            """,
        )

    with cols[1]:
        render_codeblock(
            title="Integer from 0 to 9 inclusive:",
            code="""
x = random.randrange(10)
print(x)        # example: 7
            """,
        )

        render_codeblock(
            title="Even integer from 1 to 100 inclusive:",
            code="""
x = random.randrange(1, 100)
print(x)        # example: 26
            """,
        )

        render_codeblock(
            title="Or set the step such as for even numbers",
            code="""
x = random.randrange(1, 100, 2)
print(x)        # example: 26
            """,
        )

        render_codeblock(
            title="Shuffle elements of a list",
            code="""
l = [1, 2, 3, 4]
random.shuffle(l)
print(l)
            """,
        )

    with cols[2]:
        render_codeblock(
            "Single random element from a sequence",
            """
x = random.choice(['win', 'lose', 'draw'])
print(x)        # example: 'lose'
            """,
        )
