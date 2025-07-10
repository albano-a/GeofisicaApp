import streamlit as st


def render_base():
    cols = st.columns(3)

    with cols[0]:
        st.subheader("Básico")
        st.write("##### Print to the screen:")
        st.code(
            """print("Hello World")\n""" """print("2025")""",
            language="python",
            line_numbers=True,
        )

        st.write("##### Declaring a variable")
        st.code(
            "x = 2 \ny = 3 \nprint(x) # output: 2 \nprint(y) # output: 3",
            language="python",
            line_numbers=True,
        )

        st.write("##### Tipos de variáveis")
        st.code(
            """x = 10       # int\npi = 3.14    # float\nnome = "Ana" # string\nvivo = True  # bool
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Listas")
        st.code(
            """
frutas = ["Maçã", "Pêssego", "Abacate"]
print(frutas)
# output: ["Maçã", "Pêssego", "Abacate"]
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Dicionário")
        st.code(
            """
pessoa = {
    "nome": "João",
    "idade": 30
}
print(pessoa["nome"])
# output: João
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Operador lógico")
        st.code(
            """
x = 5
print(x > 3 and x < 10)  # output: True
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Input do usuário")
        st.code(
            """
nome = input("Digite seu nome: ")
print(f"Olá, {nome}!")
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Concatenação e Replicação")
        st.code(
            """
print('Alice' * 5)
# output: 'AliceAliceAliceAliceAlice'
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Número de elementos")
        st.code(
            """
len('hello') # LENgth
# output: 5
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### for")
        st.code(
            """
for i in range(5):
    print(i)
# output:
# 0
# 1
# 2
# 3
# 4
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### while")
        st.code(
            """
n = 0
while n < 3:
    print(n)
    n += 1
# output:
# 0
# 1
# 2
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Atribuição composta")
        st.code(
            """
n = 1
n += 1 # n = n + 1
print(n)
# output: 2
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Conversão de Tipos")
        st.code(
            """
a = "10" # str
b = int(a)
print(b + 5)  # output: 15
            """,
            language="python",
            line_numbers=True,
        )

    with cols[1]:
        st.subheader("Medium level")

        st.write("##### Conditionals")
        st.code(
            """
age = 18
if age >= 18:
    print("Adult")
else:
    print("Underage")
# output: Adult
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Defining a function")
        st.code(
            """
def add(a, b):
    s = a + b
    return s       # returns a value to 

print(add(2, 3))  # output: 5
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Lists and iteration")
        st.code(
            """
numbers = [1, 2, 3, 4]
for number in numbers:
    print(number * 2)
# prints each number of the list doubled
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### list comprehension")
        quadrados = [xx**2 for xx in range(5)]
        st.code(
            f"""
quadrados = [x**2 for x in range(5)]
# output: {quadrados}
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Loop with index and value")
        st.code(
            """
lista = ["a", "b", "c"]
for i, val in enumerate(lista):
    print(i, val)
# output:
# 0 a
# 1 b
# 2 c
            """,
            language="python",
            line_numbers=True,
        )

    with cols[2]:
        st.subheader("Advanced level")

        st.write("##### Invert strings")
        st.code(
            """
texto = "Olá, Python"
print(texto[::-1])
# output: nohtyP ,álO""",
            language="python",
            line_numbers=True,
        )

        st.write("##### Quickly change two variables")
        st.code(
            """
a = 3
b = 4
a, b = b, a
# a becomes 4
# b becomes 3
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Loop over two lists simultaneously")
        st.code(
            """
names = ["A", "B", "C"]
grades = ["10", "9", "7"]
for nome, nota in zip(names, grades):
    print(f"{nome}: {nota}")
# output:
# A: 10
# B: 9
# C: 7
            """,
            language="python",
            line_numbers=True,
        )
