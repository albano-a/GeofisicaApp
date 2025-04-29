import os
import io
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


@st.cache_data
def load_data():
    return pd.read_csv("assets/data/mineral_identifier.csv")


def sort_list(df, column_name):
    """
    Sorts and returns a list of unique, lowercase substrings from a specified column in a dataframe.
    """
    return sorted(
        list(set(l.lower() for array in df[column_name] for l in array.split("-")))
    )


def get_property_input(dataframe, property_name, help=None):
    prop_in = st.selectbox(
        property_name.capitalize(),
        options=["Não sei"] + sort_list(dataframe, property_name),
        help=help,
    )
    return prop_in


def display_data(results, filter):
    df_result = pd.DataFrame(results)
    df_result = df_result[df_result["Match (%)"] > 0]
    df_result = df_result.sort_values(by="Match (%)", ascending=False)

    def colorize_match(val):
        if val > 80:
            return "background-color: #1c3d2b; color: #dffde9"
        elif val >= 60:
            return "background-color: #fff2cc; color: #7f6000"
        else:
            return "background-color: #f4cccc; color: #990000"

    if not df_result.empty:

        df_result = df_result[df_result["Match (%)"] >= filter]

        df_result_styled = df_result.style.applymap(
            colorize_match, subset=["Match (%)"]
        )

        st.success("Minerais compatíveis encontrados:")
        st.dataframe(df_result_styled)

    else:
        st.warning("Nenhum mineral encontrado com essas características.")


def run():
    df = load_data()

    cor_in = get_property_input(df, property_name="cor")
    brilho_in = get_property_input(df, property_name="brilho")
    fratura_in = get_property_input(df, property_name="fratura")
    habito_in = get_property_input(df, property_name="hábito")
    diafaneidade_in = get_property_input(df, property_name="diafaneidade")
    sistema_cristalino_in = get_property_input(df, property_name="sistema cristalino")
    clivagem_in = get_property_input(
        df,
        property_name="clivagem",
        help="Clivagem é a forma como o mineral se divide.",
    )

    st.html("<hr>")
    dureza_in = st.slider(
        "Dureza (escala Mohs)",
        1.0,
        10.0,
        step=0.5,
        help="Dureza é a resistência do mineral à abrasão",
    )

    st.html("<hr>")
    use_density = st.checkbox("Considerar densidade?")
    dens_in = st.slider("Densidade (g/cm³)", 1.0, 25.0, step=0.1)

    st.html("<hr>")
    use_magnetism = st.checkbox("Considerar magnetismo?")
    magnet_in = st.selectbox(
        "O mineral é magnético?", options=["Não", "Sim", "Não sei"]
    )

    filtrar_50 = st.slider(
        "Mostrar apenas resultados com match maior que:", 30.0, 100.0, step=0.5
    )

    # Define weights

    if st.button("Identificar"):
        resultados = []

        for _, row in df.iterrows():
            score, total = 0, 0

            # Matching logic
            def match_and_score(attribute, input_value, weight):
                nonlocal score, total
                if input_value != "Não sei":
                    total += weight
                    if input_value == row[attribute]:
                        score += weight

            # Cor (mandatory)
            total += 1
            if cor_in.lower() in str(row["cor"]).lower():
                score += PESOS["cor"]

            # Match optional attributes
            match_and_score("brilho", brilho_in, PESOS["brilho"])
            match_and_score("fratura", fratura_in, PESOS["fratura"])
            match_and_score("hábito", habito_in, PESOS["hábito"])
            match_and_score(
                "sistema cristalino", sistema_cristalino_in, PESOS["sistema cristalino"]
            )
            match_and_score("clivagem", clivagem_in, PESOS["clivagem"])
            match_and_score("diafaneidade", diafaneidade_in, PESOS["diafaneidade"])

            # Dureza
            try:
                min_dur, max_dur = map(float, str(row["dureza"]).split("-"))
                total += PESOS["dureza"]
                if min_dur <= dureza_in <= max_dur:
                    score += PESOS["dureza"]
            except:
                pass

            # Densidade
            if use_density:
                try:
                    min_dens, max_dens = map(float, str(row["densidade"]).split("-"))
                    total += PESOS["densidade"]
                    if min_dens <= dens_in <= max_dens:
                        score += PESOS["densidade"]
                except:
                    pass

            # Magnetismo
            if use_magnetism and magnet_in != "Não sei":
                total += PESOS["magnetismo"]
                if str(row["magnetismo"]).lower() == magnet_in.lower():
                    score += PESOS["magnetismo"]

            # Penalize if color doesn't match
            if cor_in.lower() not in str(row["cor"]).lower():
                score -= PESOS["cor"] * 0.1

            # Calculate match percentage
            match_pct = (score / total) * 100 if total > 0 else 0

            resultados.append(
                {
                    "Nome": row["nome"],
                    "Match (%)": round(match_pct, 1),
                    "Cor": row["cor"],
                    "Brilho": row["brilho"],
                    "Dureza": row["dureza"],
                    "Sistema Cristalino": row["sistema cristalino"],
                    "Clivagem": row["clivagem"],
                    "Fratura": row["fratura"],
                    "Diafaneidade": row["diafaneidade"],
                    "Hábito": row["hábito"],
                    "Densidade": row.get("densidade", "N/A"),
                    "Magnético": row.get("magnetismo", "N/A"),
                }
            )

        # Display results
        display_data(results=resultados, filter=filtrar_50)
