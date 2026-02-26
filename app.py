import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais")

arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

if arquivo:

    try:
        # Lê o Excel inteiro
        excel = pd.ExcelFile(arquivo, engine="openpyxl")
        abas = excel.sheet_names

        # Lê sempre a primeira aba válida
        df = pd.read_excel(excel, sheet_name=abas[0])

        # Remove linhas completamente vazias
        df = df.dropna(how="all")

        # Converte tudo que for possível para número
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="ignore")

        # Detecta automaticamente apenas colunas numéricas
        df_numeros = df.select_dtypes(include=["number"])

        if df_numeros.empty:
            st.error("Nenhuma coluna numérica detectada no arquivo.")
        else:
            st.success("Arquivo carregado com sucesso!")
            st.write("Colunas numéricas detectadas:")
            st.write(df_numeros.columns.tolist())
            st.dataframe(df_numeros.head())

            loteria = st.selectbox(
                "Escolha a Loteria:",
                ["Mega-Sena", "
