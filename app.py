# EXTREMO MASTER IA PRO - VERSÃO 4000 CORREÇÃO ABSOLUTA

import streamlit as st
import pandas as pd
import random
import re
from io import BytesIO

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.markdown("### Versão 4000 - Leitura Totalmente Segura")

CONFIG = {
    "Mega-Sena": {"faixa": 60, "qtd": 6},
    "Lotofácil": {"faixa": 25, "qtd": 15},
    "Quina": {"faixa": 80, "qtd": 5},
    "Lotomania": {"faixa": 100, "qtd": 20},
}

def extrair_numeros(valor):
    try:
        texto = str(valor)
        numeros = re.findall(r'\d+', texto)
        return [int(n) for n in numeros if 1 <= int(n) <= 100]
    except:
        return []

def processar_arquivo(uploaded_file):
    try:
        # Lê como bytes primeiro
        bytes_data = uploaded_file.read()
        excel = pd.ExcelFile(BytesIO(bytes_data))

        todos_numeros = []

        for sheet in excel.sheet_names:
            df = excel.parse(sheet)

            # Converte tudo para string manualmente
            df = df.astype(str)

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
