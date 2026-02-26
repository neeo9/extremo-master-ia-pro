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

        # Remove linhas completamente vazias
        df = df.dropna(how="all")

        # Função para extrair apenas dígitos
        def extrair_numeros(celula):
            if pd.isna(celula):
                return pd.NA
            # Remove tudo que não é número
            numeros = re.findall(r'\d+', str(celula))
            if numeros:
                return int(numeros[0])
            else:
                return pd.NA

        # Aplica a função em todo o DataFrame
        df_numeros = df.applymap(extrair_numeros)

        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df_numeros.head(10))

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
