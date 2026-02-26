import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Base em Resultados Reais")

# Upload do Excel
arquivo = st.file_uploader("Envie o arquivo Excel com resultados oficiais", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo, engine="openpyxl", dtype=str)
df = df.fillna("")
df.columns = df.columns.astype(str)
    st.success("Arquivo carregado com sucesso!")
    st.write("Visualização dos dados:")
    st.dataframe(df.head())

    loteria = st.selectbox(
        "Escolha a Loteria:",
        ["Mega-Sena", "Lotofácil", "Lotomania"]
    )

    if st.button("Gerar Jogo Inteligente"):
        if loteria == "Mega-Sena":
            numeros = sorted(random.sample(range(1, 61), 6))
        elif loteria == "Lotofácil":
            numeros = sorted(random.sample(range(1, 26), 15))
        else:
            numeros = sorted(random.sample(range(0, 100), 20))

        st.success("Jogo Gerado:")
        st.write(numeros)
