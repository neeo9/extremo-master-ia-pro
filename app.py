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

        # Função que retorna uma lista de números válidos de cada célula
        def extrair_numeros_lista(celula):
            if pd.isna(celula):
                return []
            # Extrai todos os dígitos na célula
            numeros = re.findall(r'\d+', str(celula))
            return [int(n) for n in numeros] if numeros else []

        # Aplica função em todo o dataframe
        df_listas = df.applymap(extrair_numeros_lista)

        st.success("Arquivo carregado com sucesso!")
        st.write("Visualização das primeiras 10 linhas (listas de dezenas extraídas):")
        st.dataframe(df_listas.head(10))

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
