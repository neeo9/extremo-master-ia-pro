import streamlit as st
import pandas as pd
import sys
import os

# ===============================
# CORREÇÃO DE PATH (IMPORT CORE)
# ===============================
sys.path.append(os.path.abspath("."))

from core.engine import executar_modelo


# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="EXTREMO MASTER IA PRO",
    layout="wide"
)

st.title("EXTREMO MASTER IA PRO")
st.markdown("Sistema Genético + Monte Carlo + Bayesiano")


# ===============================
# ESCOLHA DA LOTERIA
# ===============================
loteria = st.selectbox(
    "Escolha a Loteria:",
    ["MEGA-SENA", "LOTOFACIL", "QUINA", "LOTOMANIA"]
)


# ===============================
# UPLOAD DE ARQUIVO
# ===============================
uploaded_file = st.file_uploader(
    "Envie o arquivo Excel com resultados",
    type=["xlsx"]
)


# ===============================
# PROCESSAMENTO
# ===============================
if uploaded_file is not None:

    try:
        # 🔥 LEITURA 100% SEGURA (resolve erro do "-")
        df = pd.read_excel(uploaded_file, dtype=str)

        st.success("Arquivo carregado com sucesso!")

        if st.button("Gerar Palpites Inteligentes"):

            with st.spinner("Processando modelo avançado..."):

                jogos, estado, performance = executar_modelo(df, loteria)

            st.success("Palpites gerados com sucesso!")

            # ===============================
            # EXIBIÇÃO DOS JOGOS
            # ===============================
            st.subheader("Palpites Gerados:")

            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {jogo}")

            # ===============================
            # ESTADO DO MODELO
            # ===============================
            st.subheader("Estado do Modelo:")
            st.write(estado)

            # ===============================
            # PERFORMANCE
            # ===============================
            st.subheader("Performance Monte Carlo:")
            st.write(performance)

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {str(e)}")
