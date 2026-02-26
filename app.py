import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")

st.title("EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais")

arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

if arquivo is not None:

    try:
        excel = pd.ExcelFile(arquivo, engine="openpyxl")
        df = pd.read_excel(excel, sheet_name=0)

        # Remove linhas totalmente vazias
        df = df.dropna(how="all")

        # Substitui hífen por vazio
        df = df.replace("-", "")

        # Converte para número apenas o que for possível
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Mantém apenas colunas numéricas
        df_numeros = df.select_dtypes(include=["number"])

        if df_numeros.empty:
            st.error("Nenhuma coluna numerica detectada.")
        else:
            st.success("Arquivo carregado com sucesso.")
            st.dataframe(df_numeros.head())

            loteria = st.selectbox(
                "Escolha a Loteria:",
                [
                    "Mega-Sena",
                    "Lotofacil",
                    "Quina",
                    "Lotomania"
                ]
            )

            if st.button("Gerar Jogo Inteligente"):

                if loteria == "Mega-Sena":
                    numeros = sorted(random.sample(range(1, 61), 6))

                elif loteria == "Lotofacil":
                    numeros = sorted(random.sample(range(1, 26), 15))

                elif loteria == "Quina":
                    numeros = sorted(random.sample(range(1, 81), 5))

                elif loteria == "Lotomania":
                    numeros = sorted(random.sample(range(0, 100), 20))

                st.success("Jogo Gerado:")
                st.write(numeros)

    except Exception as e:
        st.error("Erro ao processar o arquivo.")
        st.write(str(e))
