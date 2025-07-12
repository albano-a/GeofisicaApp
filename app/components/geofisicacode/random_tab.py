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
    st.write(
        "Each code snippet generates a different value every time you refresh the page, so the example output may change."
    )

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

        x = random.random()

        render_codeblock(
            title="Random float between 0 and 1",
            code=f"""
x = random.random()
print(x)  # example: {x}
            """,
        )

        x = random.uniform(2.5, 10.0)

        render_codeblock(
            title="Random float: 2.5 <= x < 10",
            code=f"""
x = random.uniform(2.5, 10.0)
print(x) # example: {x}
            """,
        )

        x = random.expovariate(1 / 5)

        render_codeblock(
            title="Interval between arrivals averaging 5 seconds",
            code=f"""
x = random.expovariate(1 / 5)
print(x) # example: {x}
            """,
        )

    with cols[1]:
        x = random.randrange(10)
        render_codeblock(
            title="Integer from 0 to 9 inclusive:",
            code=f"""
x = random.randrange(10)
print(x)        # example: {x}
            """,
        )

        x = random.randrange(1, 100)

        render_codeblock(
            title="Even integer from 1 to 100 inclusive:",
            code=f"""
x = random.randrange(1, 100)
print(x)        # example: {x}
            """,
        )

        x = random.randrange(1, 100, 2)

        render_codeblock(
            title="Or set the step such as for even numbers",
            code=f"""
x = random.randrange(1, 100, 2)
print(x)        # example: {x}
            """,
        )

        l = [1, 2, 3, 4]
        random.shuffle(l)

        render_codeblock(
            title="Shuffle elements of a list",
            code=f"""
l = [1, 2, 3, 4]
random.shuffle(l)
print(l)        # example: {l}
            """,
        )

    with cols[2]:
        x = random.choice(["win", "lose", "draw"])
        y = random.choice("abcdef")

        render_codeblock(
            "Single random element from a sequence",
            f"""
x = random.choice(['win', 'lose', 'draw'])
print(x)        # example: {x}

y = random.choice('abcdef')
print(y)        # example: {y}
            """,
        )
        if st.button("Test the `choice` method", use_container_width=True):
            x = random.choice(["win", "lose", "draw"])
            st.write(f"Choice between `win`, `lose` and `draw`: `{x}`")

        c = random.choices(["win", "lose", "draw"])
        c1 = random.choices(["win", "lose", "draw"], k=2)

        render_codeblock(
            "Similar to `choice` but choices accept an optional count to return",
            f"""
c = random.choices(['win', 'lose', 'draw'])
print(c)        # example: {c}

c1 = random.choices(['win', 'lose', 'draw'], k=2)
print(c1)       # example: {c1}
            """,
        )

        s = random.sample([10, 20, 30, 40, 50], k=4)

        render_codeblock(
            "Four samples without replacement",
            f"""
s = random.sample([10, 20, 30, 40, 50], k=4)
print(s)        # example: {s}
            """,
        )

