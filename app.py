import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")

st.title("EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais")

arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

if arquivo is not None:
    try:
        # Lê tudo como string, sem cabeçalho
        df = pd.read_excel(arquivo, engine="openpyxl", header=None, dtype=str)

        # Substitui hífen ou qualquer outro caractere que não seja número
        df = df.replace(r"[^0-9]", "", regex=True)

        # Remove linhas completamente vazias
        df = df.dropna(how="all")

        # Mantém apenas as colunas das dezenas (até 20 colunas)
        df_dezenas = df.iloc[:, 2:22]  # geralmente começa na coluna 3
        # Converte cada célula para inteiro se for dígito
        for col in df_dezenas.columns:
            df_dezenas[col] = df_dezenas[col].apply(lambda x: int(x) if x.isdigit() else pd.NA)

        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df_dezenas.head())

        loteria = st.selectbox(
            "Escolha a Loteria:",
            ["Mega-Sena", "Lotofacil", "Quina", "Lotomania"]
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
