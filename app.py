import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Extremo Master IA PRO - Monte Carlo", layout="centered")
st.title("EXTREMO MASTER IA PRO - Monte Carlo")
st.write("Sistema Inteligente com Resultados Oficiais, Ciclo das Dezenas e Simulação Monte Carlo")

# ===================== UPLOAD =====================
arquivo = st.file_uploader("Envie o arquivo Excel oficial da loteria", type=["xlsx"])

loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofacil", "Quina", "Lotomania"]
)

parametros = {
    "Mega-Sena": {"min": 1, "max": 60, "qtd": 6, "top": 5},
    "Lotofacil": {"min": 1, "max": 25, "qtd": 15, "top": 15},
    "Quina": {"min": 1, "max": 80, "qtd": 5, "top": 5},
    "Lotomania": {"min": 0, "max": 99, "qtd": 20, "top": 20}
}

# ===================== FUNÇÕES =====================
def extrair_numeros_lista(celula):
    if pd.isna(celula):
        return []
    numeros = [int(n) for n in re.findall(r'\d+', str(celula))]
    # Limites por loteria
    if loteria == "Lotomania":
        numeros = [n for n in numeros if 0 <= n <= 99]
    elif loteria == "Mega-Sena":
        numeros = [n for n in numeros if 1 <= n <= 60]
    elif loteria == "Quina":
        numeros = [n for n in numeros if 1 <= n <= 80]
    elif loteria == "Lotofacil":
        numeros = [n for n in numeros if 1 <= n <= 25]
    return numeros

# ===================== PROCESSAMENTO =====================
df_numeros = None
if arquivo is not None:
    try:
        df = pd.read_excel(arquivo, engine="openpyxl", header=None, dtype=str)
        df = df.dropna(how="all")
        df = df.applymap(lambda x: x if x and re.search(r'\d', str(x)) else None)
        df_numeros = df.applymap(extrair_numeros_lista)
        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df_numeros.head(10))
    except Exception as e:
        st.error("Erro ao processar o arquivo.")
        st.write(str(e))

# ===================== CICLO DAS DEZENAS =====================
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

# ===================== FILTROS INTELIGENTES =====================
def valido_jogo(jogo):
    # Evita muitos números consecutivos
    consecutivos = sum([1 for i in range(1, len(jogo)) if jogo[i] - jogo[i-1] == 1])
    if consecutivos > 2:
        return False
    # Limita pares e ímpares
    pares = sum([1 for n in jogo if n % 2 == 0])
    impares = len(jogo) - pares
    if loteria == "Mega-Sena" and (pares < 2 or impares < 2):
        return False
    return True

# ===================== MONTE CARLO INTELIGENTE =====================
def monte_carlo(df_hist, n_sim=500):
    if df_hist is not None:
        ciclos = calcular_ciclo(df_hist)
        freq = {}
        for col in df_hist.columns:
            for lista in df_hist[col]:
                if lista:
                    for n in lista:
                        freq[n] = freq.get(n, 0) + 1
        if loteria == "Mega-Sena":
            dezenas_ouro = sorted(freq, key=freq.get, reverse=True)[:5]
        else:
            dezenas_ouro = sorted(freq, key=freq.get, reverse=True)[:parametros[loteria]["top"]]
    else:
        ciclos = {i:0 for i in range(parametros[loteria]["min"], parametros[loteria]["max"]+1)}
        dezenas_ouro = []

    melhores_jogos = []
    tentativas = 0
    while len(melhores_jogos) < 3 and tentativas < 2000:
        candidatos = []
        for _ in range(n_sim):
            jogo = []
            # Adiciona dezenas de ouro
            if loteria == "Mega-Sena":
                jogo.extend(dezenas_ouro)
            elif dezenas_ouro:
                ouro_jogo = random.sample(
                    dezenas_ouro, min(len(dezenas_ouro), parametros[loteria]["qtd"]//2)
                )
                jogo.extend(ouro_jogo)
            # Completa com números aleatórios ponderados pelo ciclo
            while len(jogo) < parametros[loteria]["qtd"]:
                n = random.randint(parametros[loteria]["min"], parametros[loteria]["max"])
                if n not in jogo:
                    peso = 1 + ciclos.get(n,0)/max(ciclos.values()) if ciclos else 1
                    if random.random() < peso:
                        jogo.append(n)
            jogo.sort()
            if valido_jogo(jogo):
                candidatos.append(jogo)
        # Escolhe os melhores 3 jogos distintos
        for c in candidatos:
            if c not in melhores_jogos and len(melhores_jogos) < 3:
                melhores_jogos.append(c)
        tentativas += 1
    return melhores_jogos

# ===================== BOTÃO =====================
if st.button("Gerar 3 Jogos Inteligentes"):
    if df_numeros is not None:
        jogos = monte_carlo(df_numeros, n_sim=500)
    else:
        # Se sem histórico, gera aleatório + filtros
        jogos = []
        while len(jogos) < 3:
            numeros = sorted(random.sample(range(parametros[loteria]["min"], parametros[loteria]["max"]+1),
                                           parametros[loteria]["qtd"]))
            if valido_jogo(numeros) and numeros not in jogos:
                jogos.append(numeros)
    st.success("Jogos Gerados Inteligentes:")
    for idx, jogo in enumerate(jogos, start=1):
        st.write(f"Jogo {idx}: {jogo}")
