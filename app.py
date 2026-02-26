import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")
st.title("EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais e Ciclo das Dezenas")

# Upload de arquivo
arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

# Função para extrair números válidos (ignora hífen e caracteres inválidos)
def extrair_numeros_lista(celula):
    if pd.isna(celula):
        return []
    numeros = re.findall(r'\d+', str(celula))
    return [int(n) for n in numeros] if numeros else []

df_numeros = None
if arquivo is not None:
    try:
        df = pd.read_excel(arquivo, engine="openpyxl", header=None, dtype=str)
        df = df.dropna(how="all")
        df_numeros = df.applymap(extrair_numeros_lista)
        st.success("Arquivo carregado com sucesso!")
        st.write("Visualização das primeiras linhas
