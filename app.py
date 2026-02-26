import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")

st.title("EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais")

arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

if arquivo is not None:
    try:
        # Lê tudo como string, sem cabeçalho
        df = pd.read_excel(arquivo, engine="openpyxl", header=None, dtype=str)

        # Remove linhas totalmente vazias
        df = df.dropna(how="all")

        # Função para extrair números válidos
        def extrair_numeros(celula):
            if pd.isna(celula):
                return pd.NA
            numeros = re.findall(r'\d+', str(celula))
            return int(numeros[0]) if numeros else pd.NA

        # Aplica função em todo o dataframe
        df_numeros = df.applymap(extrair_numeros)

        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df_numeros.head(10))

        loteria = st.selectbox(
            "Escolha a Loteria:",
            ["Mega-Sena", "Lotofacil", "Quina", "Lotomania"]
        )

        if st.button("Gerar 3 Jogos Inteligentes"):
            jogos = []
            for _ in range(3):
                if loteria == "Mega-Sena":
                    numeros = sorted(random.sample(range(1, 61), 6))
                elif loteria == "Lotofacil":
                    numeros = sorted(random.sample(range(1, 26), 15))
                elif loteria == "Quina":
                    numeros = sorted(random.sample(range(1, 81), 5))
                elif loteria == "Lotomania":
                    numeros = sorted(random.sample(range(0, 100), 20))
                jogos.append(numeros)

            st.success("Jogos Gerados:")
            for idx, jogo in enumerate(jogos, start=1):
                st.write(f"Jogo {idx}: {jogo}")

    except Exception as e:
        st.error("Erro ao processar o arquivo.")
        st.write(str(e))
