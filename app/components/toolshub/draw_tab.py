import streamlit as st
import qrcode.constants
import streamlit as st
from components.header import render_header
import random
import pandas as pd
import qrcode
import io


def render_draw():
    st.subheader("Draw names, numbers, or any item.")

    draw_type = st.selectbox("Choose the type of draw:", ["Names/Items", "Numbers"])

    unique = st.checkbox("Avoid repetitions?", value=True)
    quantity = st.number_input("Number of draws:", min_value=1, max_value=1000, value=1)

    if "history" not in st.session_state:
        st.session_state.history = set()

    def reset_history():
        st.session_state.history.clear()

    if draw_type == "Names/Items":
        option = st.radio(
            "How would you like to provide the items?",
            ["Enter manually", "Upload file (.txt, .csv)"],
        )

        items_list = []

        if option == "Enter manually":
            text = st.text_area("Enter the items (one per line):")
            if text:
                items_list = [i.strip() for i in text.splitlines() if i.strip()]
        else:
            uploaded_file = st.file_uploader("Upload the file:", type=["txt", "csv"])
            if uploaded_file:
                ext = uploaded_file.name.split(".")[-1]
                if ext == "txt":
                    data = uploaded_file.read().decode("utf-8")
                    items_list = [i.strip() for i in data.splitlines() if i.strip()]

                elif ext == "csv":
                    df = pd.read_csv(uploaded_file)
                    col = st.selectbox("Choose the column:", df.columns)
                    items_list = df[col].dropna().astype(str).tolist()

        if items_list:
            unique_items = list(set(items_list)) if unique else items_list
            remaining = (
                list(set(unique_items) - st.session_state.history)
                if unique
                else unique_items
            )

            if not remaining:
                st.warning("All items have already been drawn.")
            elif st.button("Draw"):
                drawn_items = random.sample(remaining, min(quantity, len(remaining)))
                for item in drawn_items:
                    st.write(f"🎉 {item}")
                    st.session_state.history.add(item)

                st.success("Draw completed!")

    elif draw_type == "Numbers":
        min_val = st.number_input("Minimum value:", value=1)
        max_val = st.number_input("Maximum value:", value=100)

        if min_val >= max_val:
            st.error("The maximum value must be greater than the minimum.")
        else:
            universe = list(range(int(min_val), int(max_val) + 1))
            remaining = (
                list(set(universe) - st.session_state.history) if unique else universe
            )

            if not remaining:
                st.warning("All numbers have already been drawn.")
            elif st.button("Draw"):
                drawn_numbers = random.sample(remaining, min(quantity, len(remaining)))
                for number in drawn_numbers:
                    st.write(f"🎉 {number}")
                    st.session_state.history.add(number)
                st.success("Draw completed!")

    # Reset history
    if unique:
        st.divider()
        if st.button("🔄 Reset draw history"):
            reset_history()
            st.info("History successfully cleared.")
