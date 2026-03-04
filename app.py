# EXTREMO MASTER IA PRO - VERSÃO 3000 CORREÇÃO DEFINITIVA LOTOMANIA

import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.markdown("### Versão 3000 - Correção Definitiva Lotomania")

CONFIG = {
    "Mega-Sena": {"faixa": 60, "qtd": 6},
    "Lotofácil": {"faixa": 25, "qtd": 15},
    "Quina": {"faixa": 80, "qtd": 5},
    "Lotomania": {"faixa": 100, "qtd": 20},
}


def extrair_numeros(valor):
    try:
        texto = str(valor)

        # Extrai apenas sequências numéricas
        numeros = re.findall(r'\d+', texto)

        numeros_validos = []

        for n in numeros:
            numero = int(n)
            if 1 <= numero <= 100:
                numeros_validos.append(numero)

        return numeros_validos

    except:
        return []


def processar_arquivo(uploaded_file):
    try:
        df = pd.read_excel(
            uploaded_file,
            dtype=str,
            engine="openpyxl",
            keep_default_na=False,
            na_filter=False
        )

        todos_numeros = []

        for coluna in df.columns:
            for valor in df[coluna]:
                numeros = extrair_numeros(valor)
                todos_numeros.extend(numeros)

        if not todos_numeros:
            st.warning("Nenhum número válido encontrado.")
            return None

        frequencia = (
            pd.Series(todos_numeros)
            .value_counts()
            .sort_index()
        )

        return frequencia

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
        return None


def gerar_jogo(loteria):
    faixa = CONFIG[loteria]["faixa"]
    qtd = CONFIG[loteria]["qtd"]
    return sorted(random.sample(range(1, faixa + 1), qtd))


loteria = st.selectbox("Escolha a Loteria:", list(CONFIG.keys()))
uploaded_file = st.file_uploader("Envie o arquivo Excel com os resultados", type=["xlsx"])

if uploaded_file:
    st.success("Arquivo carregado com sucesso!")

    frequencia = processar_arquivo(uploaded_file)

    if frequencia is not None:
        st.subheader("Frequência dos números encontrados:")
        st.dataframe(frequencia)

        if st.button("Gerar Jogo Inteligente"):
            jogo = gerar_jogo(loteria)
            st.success(f"Jogo gerado: {jogo}")
