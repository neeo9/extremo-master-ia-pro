import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Extremo Master IA PRO", layout="centered")
st.title("EXTREMO MASTER IA PRO")
st.write("Sistema Inteligente com Resultados Oficiais e Ciclo das Dezenas")

# Upload de arquivo
arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

# Função definitiva para extrair números válidos (ignora hífen, espaços ou caracteres inválidos)
def extrair_numeros_lista(celula):
    """
    Retorna uma lista de números inteiros válidos.
    Ignora: células vazias, hífen '-', '--', espaços e qualquer caractere inválido.
    """
    if pd.isna(celula):
        return []
    
    texto = str(celula).strip()
    if texto in ["", "-", "--"]:
        return []
    
    numeros = []
    for n in re.findall(r'\d+', texto):
        try:
            numeros.append(int(n))
        except ValueError:
            continue
    return numeros

df_numeros = None
if arquivo is not None:
    try:
        df = pd.read_excel(arquivo, engine="openpyxl", header=None, dtype=str)
        df = df.dropna(how="all")
        df_numeros = df.applymap(extrair_numeros_lista)
        st.success("Arquivo carregado com sucesso!")
        st.write("Visualização das primeiras linhas (listas de dezenas):")
        st.dataframe(df_numeros.head(10))
    except Exception as e:
        st.error("Erro ao processar o arquivo.")
        st.write(str(e))

# Seleção da loteria
loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofacil", "Quina", "Lotomania"]
)

# Parâmetros da loteria
parametros = {
    "Mega-Sena": {"min": 1, "max": 60, "qtd": 6, "top": 6},
    "Lotofacil": {"min": 1, "max": 25, "qtd": 15, "top": 15},
    "Quina": {"min": 1, "max": 80, "qtd": 5, "top": 5},
    "Lotomania": {"min": 0, "max": 99, "qtd": 20, "top": 20}
}

# Função para calcular o ciclo das dezenas
def calcular_ciclo(df_hist):
    ciclos = {}
    for col in df_hist.columns:
        for num in range(parametros[loteria]["min"], parametros[loteria]["max"] + 1):
            ult_sorteio = df_hist[::-1].applymap(lambda x: num in x if x else False)
            if ult_sorteio.any().any():
                index = ult_sorteio[::-1].idxmax().max()
                ciclos[num] = len(df_hist) - index
            else:
                ciclos[num] = len(df_hist)
    return ciclos

# Função para gerar 3 jogos inteligentes
def gerar_jogos(df_hist):
    jogos = []

    if df_hist is not None:
        ciclos = calcular_ciclo(df_hist)
    else:
        ciclos = {i: 0 for i in range(parametros[loteria]["min"], parametros[loteria]["max"] + 1)}

    # Dezenas de Ouro: mais frequentes
    dezenas_ouro = []
    if df_hist is not None:
        freq = {}
        for col in df_hist.columns:
            for lista in df_hist[col]:
                if lista:
                    for n in lista:
                        freq[n] = freq.get(n, 0) + 1
        dezenas_ouro = sorted(freq, key=freq.get, reverse=True)[:parametros[loteria]["top"]]

    for _ in range(3):
        jogo = []
        # Adiciona dezenas de Ouro distribuídas
        if dezenas_ouro:
            ouro_jogo = random.sample(
                dezenas_ouro, min(len(dezenas_ouro), parametros[loteria]["qtd"] // 2)
            )
            jogo.extend(ouro_jogo)

        # Completa com números aleatórios equilibrando ciclo e evitando repetição
        while len(jogo) < parametros[loteria]["qtd"]:
            n = random.randint(parametros[loteria]["min"], parametros[loteria]["max"])
            if n not in jogo:
                peso = 1 + ciclos.get(n, 0) / max(ciclos.values()) if ciclos else 1
                if random.random() < peso:
                    jogo.append(n)
        jogos.append(sorted(jogo))
    return jogos

# Botão para gerar os jogos
if st.button("Gerar 3 Jogos Inteligentes"):
    if df_numeros is not None:
        jogos = gerar_jogos(df_numeros)
    else:
        jogos = []
        for _ in range(3):
            numeros = sorted(
                random.sample(
                    range(parametros[loteria]["min"], parametros[loteria]["max"] + 1),
                    parametros[loteria]["qtd"]
                )
            )
            jogos.append(numeros)

    st.success("Jogos Gerados:")
    for idx, jogo in enumerate(jogos, start=1):
        st.write(f"Jogo {idx}: {jogo}")
