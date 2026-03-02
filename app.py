import streamlit as st
import pandas as pd
from core.engine import executar_modelo

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="wide")

st.title("EXTREMO MASTER IA PRO")
st.markdown("Sistema Genético + Monte Carlo + Bayesiano")

loteria = st.selectbox(
    "Escolha a Loteria:",
    ["MEGA-SENA", "LOTOFACIL", "QUINA", "LOTOMANIA"]
)

uploaded_file = st.file_uploader("Envie o arquivo Excel com resultados", type=["xlsx"])

if uploaded_file:

    try:
        # 🔥 LEITURA 100% SEGURA
        df = pd.read_excel(uploaded_file, dtype=str)

        st.success("Arquivo carregado com sucesso!")

        if st.button("Gerar Palpites Inteligentes"):

            jogos, estado, performance = executar_modelo(df, loteria)

            st.subheader("Palpites Gerados:")

            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {jogo}")

            st.subheader("Estado do Modelo:")
            st.write(estado)

            st.subheader("Performance Monte Carlo:")
            st.write(performance)

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {str(e)}")
