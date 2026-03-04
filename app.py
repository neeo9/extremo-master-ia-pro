# EXTREMO MASTER IA PRO - VERSÃO 2000 ULTRA BLINDADA

import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.markdown("### Versão 2000 - Sistema Totalmente Blindado")

CONFIG = {
    "Mega-Sena": {"faixa": 60, "qtd": 6},
    "Lotofácil": {"faixa": 25, "qtd": 15},
    "Quina": {"faixa": 80, "qtd": 5},
    "Lotomania": {"faixa": 100, "qtd": 20},
}

# FUNÇÃO TOTALMENTE SEGURA PARA EXTRAÇÃO
def extrair_numeros(valor):
    if valor is None:
        return []

    try:
        texto = str(valor)

        # Remove absolutamente tudo que não for número
        texto_limpo = re.sub(r'[^0-9]', ' ', texto)

        partes = texto_limpo.split()

        numeros_validos = []

        for p in partes:
            try:
                numero = int(p)
                if 1 <= numero <= 100:
                    numeros_validos.append(numero)
            except:
                continue

        return numeros_validos

    except:
        return []


def processar_arquivo(uploaded_file, loteria):
    try:
        # Força leitura como texto para evitar erro com "-"
        df = pd.read_excel(uploaded_file, dtype=str)

        todos_numeros = []

        for coluna in df.columns:
            for valor in df[coluna]:
                numeros = extrair_numeros(valor)
                if numeros:
                    todos_numeros.extend(numeros)

        if len(todos_numeros) == 0:
            st.warning("Nenhum número válido encontrado no arquivo.")
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

    jogo = random.sample(range(1, faixa + 1), qtd)
    return sorted(jogo)


# INTERFACE
loteria = st.selectbox("Escolha a Loteria:", list(CONFIG.keys()))
uploaded_file = st.file_uploader("Envie o arquivo Excel com os resultados", type=["xlsx"])

if uploaded_file:
    st.success("Arquivo carregado com sucesso!")

    frequencia = processar_arquivo(uploaded_file, loteria)

    if frequencia is not None:
        st.subheader("Frequência dos números encontrados:")
        st.dataframe(frequencia)

        if st.button("Gerar Jogo Inteligente"):
            jogo = gerar_jogo(loteria)
            st.success(f"Jogo gerado: {jogo}")
