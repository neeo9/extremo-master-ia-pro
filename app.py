import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Extremo Master IA PRO - Monte Carlo", layout="centered")
st.title("EXTREMO MASTER IA PRO - Monte Carlo")
st.write("Sistema Inteligente com Resultados Oficiais, Ciclo das Dezenas e Simulação Monte Carlo")

# Upload do arquivo Excel
arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

# Função de extração segura de números
def extrair_numeros_lista(celula):
    if pd.isna(celula):
        return []
    numeros = re.findall(r'\d+', str(celula))
    return [int(n) for n in numeros]

df_numeros = None
if arquivo is not None:
    try:
        df = pd.read_excel(arquivo, engine="openpyxl", header=None, dtype=str)
        df = df.dropna(how="all")
        
        # Pré-limpeza absoluta: qualquer célula sem dígito vira None
        df = df.applymap(lambda x: x if x and re.search(r'\d', str(x)) else None)
        
        # Extrai números de forma segura
        df_numeros = df.applymap(extrair_numeros_lista)
        
        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df_numeros.head(10))
    except Exception as e:
        st.error("Erro ao processar o arquivo.")
        st.write(str(e))

# Seleção da loteria
loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofacil", "Quina", "Lotomania"]
)

parametros = {
    "Mega-Sena": {"min": 1, "max": 60, "qtd": 6, "top": 6},
    "Lotofacil": {"min": 1, "max": 25, "qtd": 15, "top": 15},
    "Quina": {"min": 1, "max": 80, "qtd": 5, "top": 5},
    "Lotomania": {"min": 0, "max": 99, "qtd": 20, "top": 20}
}

# Ciclo das dezenas
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

# Monte Carlo para gerar 3 jogos distintos
def monte_carlo(df_hist, n_sim=500):
    if df_hist is not None:
        ciclos = calcular_ciclo(df_hist)
        freq = {}
        for col in df_hist.columns:
            for lista in df_hist[col]:
                if lista:
                    for n in lista:
                        freq[n] = freq.get(n, 0) + 1
        dezenas_ouro = sorted(freq, key=freq.get, reverse=True)[:parametros[loteria]["top"]]
    else:
        ciclos = {i:0 for i in range(parametros[loteria]["min"], parametros[loteria]["max"]+1)}
        dezenas_ouro = []

    melhores_jogos = []
    tentativas = 0
    while len(melhores_jogos) < 3 and tentativas < 1000:
        candidatos = []
        for _ in range(n_sim):
            jogo = []
            if dezenas_ouro:
                ouro_jogo = random.sample(
                    dezenas_ouro, min(len(dezenas_ouro), parametros[loteria]["qtd"]//2)
                )
                jogo.extend(ouro_jogo)
            while len(jogo) < parametros[loteria]["qtd"]:
                n = random.randint(parametros[loteria]["min"], parametros[loteria]["max"])
                if n not in jogo:
                    peso = 1 + ciclos.get(n,0)/max(ciclos.values()) if ciclos else 1
                    if random.random() < peso:
                        jogo.append(n)
            candidatos.append(sorted(jogo))
        candidatos.sort(key=lambda x: sum([ciclos.get(n,0) for n in x]))
        melhor = candidatos[0]
        if melhor not in melhores_jogos:
            melhores_jogos.append(melhor)
        tentativas += 1
    return melhores_jogos

# Botão de geração
if st.button("Gerar 3 Jogos Monte Carlo"):
    if df_numeros is not None:
        jogos = monte_carlo(df_numeros, n_sim=500)
    else:
        jogos = []
        while len(jogos) < 3:
            numeros = sorted(random.sample(range(parametros[loteria]["min"], parametros[loteria]["max"]+1),
                                           parametros[loteria]["qtd"]))
            if numeros not in jogos:
                jogos.append(numeros)

    st.success("Jogos Gerados com Monte Carlo:")
    for idx, jogo in enumerate(jogos, start=1):
        st.write(f"Jogo {idx}: {jogo}")
