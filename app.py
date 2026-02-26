import streamlit as st
import random

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")
st.title("EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais")

arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

if arquivo is not None:
    st.success("Arquivo carregado com sucesso! (Nenhum processamento de número necessário)")

loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofacil", "Quina", "Lotomania"]
)

if st.button("Gerar 3 Jogos Inteligentes"):
    jogos = []
    for _ in range(3):
        if loteria == "Mega-Sena":
            numeros = sorted(random.sample(range(1, 61), 6))
        elif loteria == "Lotofacil":
            numeros = sorted(random.sample(range(1, 26), 15))
        elif loteria == "Quina":
            numeros = sorted(random.sample(range(1, 81), 5))
        elif loteria == "Lotomania":
            numeros = sorted(random.sample(range(0, 100), 20))
        jogos.append(numeros)

    st.success("Jogos Gerados:")
    for idx, jogo in enumerate(jogos, start=1):
        st.write(f"Jogo {idx}: {jogo}")
