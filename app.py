import streamlit as st
import pandas as pd
from database.db import criar_tabelas
from core.engine import executar_modelo

# Inicializa banco
criar_tabelas()

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="wide")

st.title("🔥 EXTREMO MASTER IA PRO — IA Evolutiva Institucional")

st.markdown("Sistema com GA + Monte Carlo + Reforço Bayesiano + Adaptativo Automático")

# Seleção de loteria
loteria = st.selectbox(
    "Selecione a Loteria",
    ["MEGA-SENA", "LOTOFACIL", "QUINA", "LOTOMANIA"]
)

# Upload do Excel
arquivo = st.file_uploader("Importar arquivo Excel de resultados", type=["xlsx"])

if arquivo:

    try:
        df = pd.read_excel(arquivo, engine="openpyxl")

        st.success("Arquivo carregado com sucesso.")

        if st.button("🎯 Gerar 3 Jogos Refinados Econômicos"):

            with st.spinner("IA evoluindo e simulando cenários..."):

                jogos, estado, performance = executar_modelo(df, loteria)

            st.subheader("📊 Estado Atual do Modelo")
            st.write(f"Estado: {estado}")
            st.write(f"Performance média Monte Carlo: {round(performance, 4)}")

            st.subheader("🎯 3 Jogos Refinados Econômicos")
            for i, jogo in enumerate(jogos):
                st.write(f"Jogo {i+1}: {sorted(jogo)}")

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")

else:
    st.info("Importe um arquivo Excel para iniciar.")
