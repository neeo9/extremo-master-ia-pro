# EXTREMO MASTER IA PRO - VERSÃO 5000 À PROVA DE ERROS

import streamlit as st
import pandas as pd
import random
from io import BytesIO

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.markdown("### Versão 5000 - Sistema Absolutamente Seguro")

CONFIG = {
    "Mega-Sena": {"faixa": 60, "qtd": 6},
    "Lotofácil": {"faixa": 25, "qtd": 15},
    "Quina": {"faixa": 80, "qtd": 5},
    "Lotomania": {"faixa": 100, "qtd": 20},
}


def limpar_e_extrair(valor):
    numeros = []
    numero_atual = ""

    try:
        texto = str(valor)

        for caractere in texto:
            if caractere.isdigit():
                numero_atual += caractere
            else:
                if numero_atual != "":
                    numero_int = int(numero_atual)
                    if 1 <= numero_int <= 100:
                        numeros.append(numero_int)
                    numero_atual = ""

        # captura último número se existir
        if numero_atual != "":
            numero_int = int(numero_atual)
            if 1 <= numero_int <= 100:
                numeros.append(numero_int)

    except:
        pass

    return numeros


def processar_arquivo(uploaded_file):
    try:
        bytes_data = uploaded_file.read()
        excel = pd.ExcelFile(BytesIO(bytes_data))

        todos_numeros = []

        for sheet in excel.sheet_names:
            df = excel.parse(sheet)

            for coluna in df.columns:
                for valor in df[coluna]:
                    numeros = limpar_e_extrair(valor)
                    todos_numeros.extend(numeros)

        if len(todos_numeros) == 0:
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
