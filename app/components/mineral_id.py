import uuid
import pandas as pd
import streamlit as st

PESOS = {
    "cor": 1.0,
    "brilho": 1.5,
    "fratura": 1.0,
    "hábito": 1.0,
    "dureza": 2.0,
    "densidade": 2.0,
    "magnetismo": 3.0,
    "diafaneidade": 1.5,
    "sistema cristalino": 2.0,
    "clivagem": 2.0,
}

# Defina manualmente as opções de entrada
INPUT_OPTIONS = {
    "cor": [
        "Não Sei",
        "Incolor",
        "Branco",
        "Preto",
        "Amarelo",
        "Amarelo Avermelhado",
        "Amarelo Claro",
        "Amarelo Latão",
        "Vermelho",
        "Azul",
        "Azul Claro",
        "Cinza Escuro",
        "Castanho",
        "Cinza",
        "Cinza Amarelado",
        "Cinza Azulado",
        "Cinza Aço",
        "Cinza Escuro",
        "Dourado",
        "Laranja",
        "Marrom",
        "Marrom Escuro",
        "Prata",
        "Preto Amarronzado",
        "Rosa",
        "Verde",
        "Verde Claro",
        "Verde Escuro",
        "Verde Oliva",
        "Vermelho Escuro",
        "Violeta",
    ],
    "brilho": [
        "Não sei",
        "Metálico",
        "Submetálico",
        "Vítreo",
        "Subvítreo",
        "Resinoso",
        "Sedoso",
        "Peroláceo",
        "Adamantino",
        "Opalescente",
        "Terroso",
        "Fosco",
        "Gorduroso",
        "Nacarado",
    ],
    "fratura": [
        "Não sei",
        "Conchoidal",
        "Fibrosa",
        "Estilhaçada",
        "Serrilhada",
        "Denteada",
        "Desigual",
        "Irregular",
        "Rugosa",
        "Lisa",
    ],
    "hábitos individuais": [
        "Não sei",
        "Acicular",
        "Capilar",
        "Laminado",
        "Cúbico",
        "Octaédrico",
        "Tabular",
        "Prismático",
        "Colunar",
        "Lamelar",
        "Escamoso",
        "Foliáceo",
        "Micáceo",
        "Granular",
    ],
    "hábitos agregados": [
        "Não sei",
        "Agregado foliáceo",
        "Agregado micáceo",
        "Agregado lamelar",
        "Agregado plumoso",
        "Agregado granular",
        "Agregado dendrítico",
        "Agregado reticulado",
        "Agregado divergente",
        "Agregado drusiforme",
        "Agregado colunar",
        "Agregado laminado",
        "Agregado fibroso",
        "Agregado estrelado",
        "Agregado globular",
        "Agregado botrióide",
        "Agregado colomorfo",
        "Agregado reniforme",
        "Agregado mamilar",
        "Agregado esferoidal",
    ],
    "sistema cristalino": [
        "Não sei",
        "Isométrico",
        "Monoclínico",
        "Ortorrômbico",
        "Hexagonal",
        "Trigonal",
        "Tetragonal",
        "Romboédrico",
    ],
    "clivagem": ["Não sei", "Ausente", "Indistinta", "Regular", "Boa", "Perfeita"],
    "diafaneidade": ["Não sei", "Transparente", "Translúcido", "Opaco"],
    "magnetismo": ["Não sei", "Não", "Fraco", "Moderado", "Forte"],
}


@st.cache_data
def load_data():
    df = pd.read_csv("assets/data/mineral_identifier.csv")
    return df


def get_property_input(property_name, help=None, key=None):
    options = INPUT_OPTIONS.get(property_name, ["Não sei"])
    return st.selectbox(
        property_name.capitalize(),
        options=options,
        help=help,
        key=key,
    )


def display_data(results, filter):
    df_result = pd.DataFrame(results)
    df_result = df_result[df_result["Match (%)"] > 0]
    df_result = df_result.sort_values(by="Match (%)", ascending=False)

    def colorize_match(val):
        if val >= 75:
            return "background-color: #1c3d2b; color: #dffde9"
        elif val >= 50:
            return "background-color: #fff2cc; color: #7f6000"
        else:
            return "background-color: #f4cccc; color: #990000"

    if not df_result.empty:

        df_result = df_result[df_result["Match (%)"] >= filter]
        df_result = df_result.reset_index(drop=True)

        df_result_styled = df_result.style\
            .map(colorize_match, subset=["Match (%)"])\
            .hide(axis="index")
        

        st.success("Minerais compatíveis encontrados:")
        st.dataframe(df_result_styled)

    else:
        st.warning("Nenhum mineral encontrado com essas características.")


def algorithm(df, weights, props: list):
    resultados = []

    attr_keys = [
        "cor",
        "brilho",
        "fratura",
        "hábito",
        "sistema cristalino",
        "clivagem",
        "diafaneidade",
        "dureza",
        "use_density",
        "densidade",
        "use_magnetism",
        "magnetismo",
    ]
    prop_map = dict(zip(attr_keys, props))


    
    def match_categorical(row_val, input_val):
        row_vals = [v.strip().lower() for v in str(row_val).split(";")]
        input_vals = [v.strip().lower() for v in str(input_val).split(";")]
        return any(val in row_vals for val in input_vals)

    def match_interval(row_val, user_val):
        try:
            min_v, max_v = map(float, str(row_val).split("-"))
            return min_v <= user_val <= max_v
        except:
            return False

    for _, row in df.iterrows():
        score, total = 0, 0

        # Cor é sempre avaliada
        total += weights["cor"]
        if (
            prop_map["cor"] != "Não sei"
            and prop_map["cor"].lower() in str(row["cor"]).lower()
        ):
            score += weights["cor"]
        else:
            score -= weights["cor"] * 0.1

        # Categóricos opcionais
        for attr in [
            "brilho",
            "fratura",
            "hábito",
            "sistema cristalino",
            "clivagem",
            "diafaneidade",
        ]:
            if prop_map[attr] != "Não sei":
                total += weights[attr]
                if match_categorical(row[attr], prop_map[attr]):
                    score += weights[attr]

        # Dureza
        total += weights["dureza"]
        if match_interval(row["dureza"], prop_map["dureza"]):
            score += weights["dureza"]
        else:
            score -= weights["dureza"] * 0.1

        # Densidade
        if prop_map["use_density"]:
            total += weights["densidade"]
            if match_interval(row["densidade"], prop_map["densidade"]):
                score += weights["densidade"]
            else:
                score -= weights["densidade"] * 0.1

        # Magnetismo
        if prop_map["use_magnetism"] and prop_map["magnetismo"] != "Não sei":
            total += weights["magnetismo"]
            if match_categorical(row["magnetismo"], prop_map["magnetismo"]):
                score += weights["magnetismo"]
            else:
                score -= weights["magnetismo"] * 0.1

        match_pct = (score / total) * 100 if total else 0

        resultados.append(
            {
                "Nome": row["nome"],
                "Match (%)": round(match_pct, 1),
                "Cor": row["cor"],
                "Dureza": row["dureza"],
                "Classificação": row["classificação"],
                "Brilho": row["brilho"],
                "Sistema Cristalino": row["sistema cristalino"],
                "Clivagem": row["clivagem"],
                "Fratura": row["fratura"],
                "Diafaneidade": row["diafaneidade"],
                "Hábito": row["hábito"],
                "Densidade": row.get("densidade", "N/A"),
                "Magnético": row.get("magnetismo", "N/A"),
                "Fórmula" : row["fórmula"]
            }
        )

    return resultados


def run():
    df = load_data()

    st.subheader("Propriedades Visuais")
    cor_in = get_property_input(property_name="cor")
    brilho_in = get_property_input(property_name="brilho")
    diafaneidade_in = get_property_input(property_name="diafaneidade")
    sistema_cristalino_in = get_property_input(property_name="sistema cristalino")

    st.divider()
    st.subheader("Propriedades Físicas")
    clivagem_in = get_property_input(
        property_name="clivagem",
        help="Clivagem é a forma como o mineral se divide.",
    )
    dureza_in = st.slider(
        "Dureza (escala Mohs)",
        0.0,
        10.0,
        step=0.5,
        help="Dureza é a resistência do mineral à abrasão",
    )
    fratura_in = get_property_input(property_name="fratura")
    tipo_habito = st.radio(
        "Escolha o tipo de hábito",
        options=["Cristais Individuais", "Agregados de Cristais"],
    )
    cols = st.columns(3)
    with cols[0]:
        hab1 = get_property_input(
            property_name=(
                "hábitos individuais"
                if tipo_habito == "Cristais Individuais"
                else "hábitos agregados"
            ),
            key="hab_input_1"
        )
    with cols[1]:
        hab2 = get_property_input(
            property_name=(
                "hábitos individuais"
                if tipo_habito == "Cristais Individuais"
                else "hábitos agregados"
            ),
            key="hab_input_2",
        )
    with cols[2]:
        hab3 = get_property_input(
            property_name=(
                "hábitos individuais"
                if tipo_habito == "Cristais Individuais"
                else "hábitos agregados"
            ),
            key="hab_input_3",
        )
    habito_in = "; ".join(set([h for h in [hab1, hab2, hab3] if h != "Não sei"]))
        
    use_density = st.checkbox("Considerar densidade?")
    dens_in = st.slider("Densidade (g/cm³)", 1.0, 25.0, step=0.1)
    use_magnetism = st.checkbox("Considerar magnetismo?")
    magnet_in = st.selectbox(
        "O mineral é magnético?",
        options=["Não", "Não sei", "Fraco", "Moderado", "Forte"],
    )

    filtrar_valores = st.slider(
        "Mostrar apenas resultados com match maior que:", 5.0, 100.0, step=0.5
    )

    # Define weights
    list_of_widgets = [
        cor_in,
        brilho_in,
        fratura_in,
        habito_in,
        sistema_cristalino_in,
        clivagem_in,
        diafaneidade_in,
        dureza_in,
        use_density,
        dens_in,
        use_magnetism,
        magnet_in,
    ]

    if st.button("Identificar"):
        if dureza_in == 0.0:
            st.error("Dureza é necessária.")
        else:
            resultados = algorithm(df, weights=PESOS, props=list_of_widgets)

            display_data(results=resultados, filter=filtrar_valores)
