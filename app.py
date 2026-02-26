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
        st.write("Visualização das primeiras linhas (listas de dezenas):")
        st.dataframe(df_numeros.head(10))
    except Exception as e:
        st.error("Erro ao processar o arquivo.")
        st.write(str(e))

# Seleção da loteria
loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofacil", "Quina", "Lotomania"]
)

# Parâmetros da loteria
parametros = {
    "Mega-Sena": {"min": 1, "max": 60, "qtd": 6, "top": 6},
    "Lotofacil": {"min": 1, "max": 25, "qtd": 15, "top": 15},
    "Quina": {"min": 1, "max": 80, "qtd": 5, "top": 5},
    "Lotomania": {"min": 0, "max": 99, "qtd": 20, "top": 20}
}

# Função para calcular o ciclo das dezenas (tempo desde última saída)
def calcular_ciclo(df_hist):
    ciclos = {}
    for col in df_hist.columns:
        for num in range(parametros[loteria]["min"], parametros[loteria]["max"] + 1):
            ult_sorteio = df_hist[::-1].applymap(lambda x: num in x if x else False)
            if ult_sorteio.any().any():
                index = ult_sorteio[::-1].idxmax().max()
                ciclos[num] = len(df_hist) - index
            else:
                ciclos[num] = len(df_hist)
    return ciclos

# Função para gerar 3 jogos inteligentes
def gerar_jogos(df_hist):
    jogos = []
    ciclos = calcular_ciclo(df_hist) if df_hist is not None else
