# EXTREMO MASTER IA PRO - VERSÃO 1000 BLINDADA LOTOMANIA

import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.markdown("### Versão 1000 - Lotomania 100% Corrigida")

CONFIG = {
    "Mega-Sena": {"faixa": 60, "qtd": 6},
    "Lotofácil": {"faixa": 25, "qtd": 15},
    "Quina": {"faixa": 80, "qtd": 5},
    "Lotomania": {"faixa": 100, "qtd": 20},
}

# FUNÇÃO TOTALMENTE BLINDADA
def extrair_numeros(valor):
    if pd.isna(valor):
        return []

    try:
        texto = str(valor)

        # Remove tudo que não for número
        texto_limpo = re.sub(r'[^0-9]', ' ', texto)

        partes = texto_limpo.split()

        numeros_validos = []

        for p in partes:
            try:
                num = int(p)
                if 1 <= num <= 100:
                    numeros_validos.append(num)
            except:
                continue

        return numeros_validos

    except:
        return []

def processar_arquivo(uploaded_file, loteria):
    try:
        df = pd.read_excel(uploaded_file)
        todos_numeros = []

        for col in df.columns:
            for valor in df[col]:
                numeros = extrair_numeros(valor)
                todos_numeros.extend(numeros)

        if not todos_numeros:
            st.warning("Nenhum número válido encontrado no arquivo.")
            return None

        freq = (
            pd.Series(todos_numeros)
            .value_counts()
            .sort_index()
        )

        return freq

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

    freq = processar_arquivo(uploaded_file, loteria)

    if freq is not None:
        st.subheader("Frequência dos números encontrados:")
        st.write(freq)

        if st.button("Gerar Jogo Inteligente"):
            jogo = gerar_jogo(loteria)
            st.success(f"Jogo gerado: {jogo}")
