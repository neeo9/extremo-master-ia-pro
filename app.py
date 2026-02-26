import streamlit as st
import random

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente de Geração Estatística")

loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena (6 números)", "Lotofácil (15 números)", "Lotomania (20 números)"]
)

def gerar_numeros(qtd, minimo, maximo):
    return sorted(random.sample(range(minimo, maximo + 1), qtd))

if st.button("Gerar Jogo Inteligente"):
    
    if "Mega" in loteria:
        numeros = gerar_numeros(6, 1, 60)
    elif "Lotofácil" in loteria:
        numeros = gerar_numeros(15, 1, 25)
    else:
        numeros = gerar_numeros(20, 0, 99)
    
    st.success("Jogo Gerado:")
    st.write(numeros)
