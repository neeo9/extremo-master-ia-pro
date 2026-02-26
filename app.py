import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais")

arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

if arquivo:

    try:
        # Lê todas as abas
        excel = pd.ExcelFile(arquivo, engine="openpyxl")
        abas = excel.sheet_names
        
        st.write("Abas encontradas no arquivo:", abas)

        # Lê sempre a primeira aba disponível
        df = pd.read_excel(excel, sheet_name=abas[0], dtype=str)
        df = df.fillna("")
        df.columns = df.columns.astype(str)

        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df.head())

        loteria = st.selectbox(
            "Escolha a Loteria:",
            ["Mega-Sena", "Lotofácil", "Quina", "Lotomania"]
        )

        if st.button("Gerar Jogo Inteligente"):

            if loteria == "Mega-Sena":
                numeros = sorted(random.sample(range(1, 61), 6))

            elif loteria == "Lotofácil":
                numeros = sorted(random.sample(range(1, 26), 15))

            elif loteria == "Quina":
                numeros = sorted(random.sample(range(1, 81), 5))

            elif loteria == "Lotomania":
                numeros = sorted(random.sample(range(0, 100), 20))

            st.success("Jogo Gerado:")
            st.write(numeros)

    except Exception as e:
        st.error("Erro ao ler o arquivo.")
        st.write("Detalhe do erro:")
        st.write(e)
