import streamlit as st


def render_base():
    cols = st.columns(3)

    with cols[0]:
        st.subheader("Básico")
        st.write("##### Para imprimir algo na tela, use:")
        st.code(
            """
            print("Hello World")
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Tipos de variáveis")
        st.code(
            """
            x = 10       # int
            pi = 3.14    # float
            nome = "Ana" # string
            vivo = True  # bool
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

        st.write("##### Loop for")
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

        st.write("##### Loop while")
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
            len('hello')
            # output: 5
            """,
            language="python",
            line_numbers=True,
        )

    with cols[1]:
        st.subheader("Médio")

        st.write("##### Condicionais")
        st.code(
            """
            idade = 18
            if idade >= 18:
                print("Maior de idade")
            else:
                print("Menor de idade")
            # output: Maior de idade
            """,
            language="python",
            line_numbers=True,
        )


        st.write("##### Definir uma função")
        st.code(
            """
            def soma(a, b):
                s = a + b
                return s
            print(soma(2, 3))  # output: 5
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Listas e iteração")
        st.code(
            """
            nums = [1, 2, 3, 4]
            for n in nums:
                print(n * 2)
            # output
            # 2
            # 4
            # 6
            # 8
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Criar listas de forma compacta")
        quadrados = [xx**2 for xx in range(5)]
        st.code(
            f"""
            quadrados = [x**2 for x in range(5)]
            # output: {quadrados}
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Acessar índice e valor ao mesmo tempo")
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
        st.subheader("Avançado")

        st.write("##### Para inverter strings")
        st.code(
            """
            texto = "Olá, Python"
            print(texto[::-1])
            # output: nohtyP ,álO
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Troca de valores entre variáveis, sem variável temporária")
        st.code(
            """
            a = 3
            b = 4
            a, b = b, a
            # a = 4
            # b = 3
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Iterar por duas listas ao mesmo tempo")
        st.code(
            """
            nomes = ["A", "B", "C"]
            notas = ["10", "9", "7"]
            for nome, nota in zip(nomes, notas):
                print(f"{nome}: {nota}")
            # output:
            # A: 10
            # B: 9
            # C: 7
            """,
            language="python",
            line_numbers=True,
        )
