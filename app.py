# EXTREMO MASTER IA PRO - VERSÃO 999 FINAL CORRIGIDA

import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.markdown("### Versão 999 - Correção Total Lotomania")

CONFIG = {
    "Mega-Sena": {"faixa": 60, "qtd": 6},
    "Lotofácil": {"faixa": 25, "qtd": 15},
    "Quina": {"faixa": 80, "qtd": 5},
    "Lotomania": {"faixa": 100, "qtd": 20},
}

def extrair_numeros(valor):
    if pd.isna(valor):
        return []
    
    texto = str(valor)
    
    # Remove qualquer coisa que não seja número
    numeros = re.findall(r'\d+', texto)
    
    return [int(n) for n in numeros]

def processar_arquivo(uploaded_file, loteria):
    try:
        df = pd.read_excel(uploaded_file)
        todos_numeros = []

        for col in df.columns:
            for valor in df[col]:
                numeros = extrair_numeros(valor)
                todos_numeros.extend(numeros)

        if not todos_numeros:
            return None

        freq = pd.Series(todos_numeros).value_counts().sort_values(ascending=False)
        return freq

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
        return None

def gerar_jogo(loteria):
    faixa = CONFIG[loteria]["faixa"]
    qtd = CONFIG[loteria]["qtd"]

    jogo = random.sample(range(1, faixa + 1), qtd)
    return sorted(jogo)

loteria = st.selectbox("Escolha a Loteria:", list(CONFIG.keys()))
uploaded_file = st.file_uploader("Envie o arquivo Excel com os resultados", type=["xlsx"])

if uploaded_file:
    st.success("Arquivo carregado com sucesso!")
    
    freq = processar_arquivo(uploaded_file, loteria)
    
    if freq is not None:
        st.subheader("Top 20 números mais frequentes:")
        st.write(freq.head(20))
        
        if st.button("Gerar Jogo Inteligente"):
            jogo = gerar_jogo(loteria)
            st.success(f"Jogo gerado: {jogo}")
