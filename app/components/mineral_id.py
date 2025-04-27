import os
import io
import pandas as pd
import streamlit as st


def run():
    df = pd.read_csv("assets/data/mineral_identifier.csv")

    # Extract unique colors
    cores_unicas = sorted(
        list(set(c.lower() for cor in df["cor"] for c in cor.split("-")))
    )

    # Input fields
    cor_in = st.selectbox("Cor", options=cores_unicas)
    brilho_in = st.selectbox(
        "Brilho",
        options=["Não sei"]
        + sorted(list(set(bb for bri in df["brilho"] for bb in bri.split("-")))),
    )
    fratura_in = st.selectbox(
        "Fratura",
        options=["Não sei"]
        + sorted(
            list(set(ff for frat in df["fratura"] for ff in str(frat).split("-")))
        ),
    )
    habito_in = st.selectbox(
        "Hábito",
        options=["Não sei"]
        + sorted(list(set(hh for hab in df["hábito"] for hh in hab.split("-")))),
    )
    diafaneidade_in = st.selectbox(
        "Diafaneidade",
        options=sorted(
            list(set(d for diaf in df["diafaneidade"] for d in diaf.split("-")))
        ),
        help="Diafaneidade é a propriedade do mineral de reagir a luz.",
    )
    sistema_cristalino_in = st.selectbox(
        "Sistema Cristalino",
        options=["Não sei"] + sorted(df["sistema cristalino"].dropna().unique()),
    )
    clivagem_in = st.selectbox(
        "Clivagem",
        options=["Não sei"]
        + sorted(list(set(cc for cliv in df["clivagem"] for cc in cliv.split("-")))),
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
    usar_densidade = st.checkbox("Considerar densidade?")
    dens_in = st.slider("Densidade (g/cm³)", 1.0, 25.0, step=0.1)

    st.html("<hr>")
    usar_magnetismo = st.checkbox("Considerar magnetismo?")
    magnet_in = st.selectbox(
        "O mineral é magnético?", options=["Não", "Sim", "Não sei"]
    )

    filtrar_60 = st.checkbox("Mostrar apenas resultados com match > 60%")

    # Define weights
    pesos = {
        "cor": 1,
        "brilho": 1.5,
        "fratura": 1,
        "hábito": 1,
        "dureza": 2,
        "densidade": 2,
        "magnetismo": 3,
        "diafaneidade": 1.5,
        "sistema cristalino": 2,
        "clivagem": 2,
    }

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
                score += pesos["cor"]

            # Match optional attributes
            match_and_score("brilho", brilho_in, pesos["brilho"])
            match_and_score("fratura", fratura_in, pesos["fratura"])
            match_and_score("hábito", habito_in, pesos["hábito"])
            match_and_score(
                "sistema cristalino", sistema_cristalino_in, pesos["sistema cristalino"]
            )
            match_and_score("clivagem", clivagem_in, pesos["clivagem"])
            match_and_score("diafaneidade", diafaneidade_in, pesos["diafaneidade"])

            # Dureza
            try:
                min_dur, max_dur = map(float, str(row["dureza"]).split("-"))
                total += pesos["dureza"]
                if min_dur <= dureza_in <= max_dur:
                    score += pesos["dureza"]
            except:
                pass

            # Densidade
            if usar_densidade:
                try:
                    min_dens, max_dens = map(float, str(row["densidade"]).split("-"))
                    total += pesos["densidade"]
                    if min_dens <= dens_in <= max_dens:
                        score += pesos["densidade"]
                except:
                    pass

            # Magnetismo
            if usar_magnetismo and magnet_in != "Não sei":
                total += pesos["magnetismo"]
                if str(row["magnetismo"]).lower() == magnet_in.lower():
                    score += pesos["magnetismo"]

            # Penalize if color doesn't match
            if cor_in.lower() not in str(row["cor"]).lower():
                score -= pesos["cor"] * 0.1

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
        df_result = pd.DataFrame(resultados)
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
            if filtrar_60:
                df_result = df_result[df_result["Match (%)"] >= 60]

            df_result_styled = df_result.style.applymap(
                colorize_match, subset=["Match (%)"]
            )

            st.success("Minerais compatíveis encontrados:")
            st.dataframe(df_result_styled)

        else:
            st.warning("Nenhum mineral encontrado com essas características.")
