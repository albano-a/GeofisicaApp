import streamlit as st
import pandas as pd


def render_pandas():
    cols = st.columns(3)

    with cols[0]:
        st.write("##### Import module")
        st.code(
            """
# To import any module in python, we use
import pandas           # without alias
import pandas as pd     # with alias (more common)
            """,
            language="python",
            line_numbers=True,
        )

        st.write("##### Reading data from string")
        st.write(
            """
            This can be done using either local files or external links. In this case, 
            we're using a popular machine learning training dataset provided directly by Google.
            """
        )
        url = (
            "https://storage.googleapis.com/mledu-datasets/california_housing_train.csv"
        )
        df = pd.read_csv(url)
        st.code(
            f"""
url = '{url}'
df = pd.read_csv(url)"""
        )
        st.dataframe(df)

    with cols[1]:
        st.write("##### Read CSV and show 5 first lines")
        file = st.file_uploader("Upload a CSV file", type="CSV")
        if file:
            df1 = pd.read_csv(file)
            st.code(
                f"""
df = pd.read_csv('{file.name}')
print(df.head())""",
                language="python",
                line_numbers=True,
            )
            st.dataframe(df1.head())

        st.write("##### See an overview of a Dataset")
        st.code(
            f"""
print(df.describe())"""
        )
        st.dataframe(df.describe())
        
        
        st.write("##### Statistics functions")
        columns = st.selectbox("Select a column", df.columns.tolist()[2:], key="1")
        st.code(
            f"""
max = df['{columns}'].max() # {df[columns].max()}
min = df['{columns}'].min() # {df[columns].min()}
std = df['{columns}'].std() # {df[columns].std()}
mean = df['{columns}'].mean() # {df[columns].mean()}

"""
        )

    with cols[2]:
        st.write("##### Filter by condition")
        columns = st.selectbox("Select a column", df.columns.tolist()[2:])
        value = st.slider(
            f"{columns} lower limit",
            min_value=df[columns].min(),
            value=df[columns].mean(),
            max_value=df[columns].max(),
        )
        st.write()
        housing = df[df[columns] > value]
        st.code(
            f"""
rooms = df[df['{columns}'] > {value}]
print(rooms)""",
            language="python",
            line_numbers=True,
        )
        st.dataframe(housing)

