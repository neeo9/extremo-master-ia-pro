# EXTREMO MASTER IA PRO - VERSÃO 9500 COM PADRÃO CONDICIONAL

import streamlit as st
import requests
import pandas as pd
import random
from collections import defaultdict

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="centered")

st.title("🔥 EXTREMO MASTER IA PRO")
st.markdown("### EXTREMO MASTER REAL + PADRÃO CONDICIONAL")

CONFIG = {
    "Mega-Sena": {"faixa": 60, "qtd": 6, "url": "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/"},
    "Lotofácil": {"faixa": 25, "qtd": 15, "url": "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/"},
    "Quina": {"faixa": 80, "qtd": 5, "url": "https://servicebus2.caixa.gov.br/portaldeloterias/api/quina/"},
    "Lotomania": {"faixa": 100, "qtd": 20, "url": "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotomania/"},
}

# -----------------------------------
# BUSCAR HISTÓRICO COMPLETO
# -----------------------------------

def buscar_historico(loteria):
    base_url = CONFIG[loteria]["url"]
    historico = []
    concurso = 1

    while True:
        try:
            r = requests.get(base_url + str(concurso), timeout=5)
            if r.status_code != 200:
                break

            dados = r.json()
            if "listaDezenas" not in dados:
                break

            dezenas = [int(n) for n in dados["listaDezenas"]]
            historico.append(dezenas)
            concurso += 1

        except:
            break

    return historico

# -----------------------------------
# CORRELAÇÃO CONDICIONAL
# -----------------------------------

def calcular_correlacao_condicional(historico):
    ocorrencias = defaultdict(int)
    pares = defaultdict(int)

    for concurso in historico:
        for x in concurso:
            ocorrencias[x] += 1
            for y in concurso:
                if x != y:
                    pares[(x, y)] += 1

    correlacao = {}

    for (x, y), count in pares.items():
        correlacao[(x, y)] = count / ocorrencias[x]

    return correlacao

# -----------------------------------
# GERADOR EXTREMO MASTER + CONDICIONAL
# -----------------------------------

def gerar_jogo_extremo(loteria, historico, correlacao):
    faixa = CONFIG[loteria]["faixa"]
    qtd = CONFIG[loteria]["qtd"]

    # Frequência total
    todas = [n for concurso in historico for n in concurso]
    freq = pd.Series(todas).value_counts()
    freq = freq.reindex(range(1, faixa+1), fill_value=0)

    numeros = list(range(1, faixa+1))
    pesos = [freq[n] + 1 for n in numeros]

    jogo = []

    # Escolhe primeiro número ponderado
    primeiro = random.choices(numeros, weights=pesos, k=1)[0]
    jogo.append(primeiro)

    # Demais números usando correlação condicional
    while len(jogo) < qtd:
        candidatos = []

        for n in numeros:
            if n not in jogo:
                score = sum(correlacao.get((x, n), 0) for x in jogo)
                candidatos.append((n, score))

        candidatos.sort(key=lambda x: x[1], reverse=True)

        if candidatos and candidatos[0][1] > 0:
            jogo.append(candidatos[0][0])
        else:
            n = random.choice([x for x in numeros if x not in jogo])
            jogo.append(n)

    jogo = sorted(jogo)

    # Filtro anti sequência
    if any(jogo[i] + 1 == jogo[i+1] for i in range(len(jogo)-1)):
        return gerar_jogo_extremo(loteria, historico, correlacao)

    return jogo

# -----------------------------------
# INTERFACE
# -----------------------------------

loteria = st.selectbox("Escolha a Loteria:", list(CONFIG.keys()))

if st.button("ATIVAR EXTREMO MASTER + PADRÃO CONDICIONAL"):

    with st.spinner("Buscando histórico completo..."):
        historico = buscar_historico(loteria)

    if not historico:
        st.error("Erro ao carregar histórico.")
    else:
        st.success(f"{len(historico)} concursos carregados!")

        with st.spinner("Calculando correlação condicional..."):
            correlacao = calcular_correlacao_condicional(historico)

        st.subheader("🎯 3 Jogos SUPER OTIMIZADOS:")

        jogos = []

        for i in range(3):
            jogo = gerar_jogo_extremo(loteria, historico, correlacao)
            jogos.append(jogo)
            st.success(f"Jogo {i+1}: {jogo}")

        st.subheader("📊 Exemplo de Tabela Condicional (Top 10):")

        top_condicional = sorted(correlacao.items(), key=lambda x: x[1], reverse=True)[:10]

        df_cond = pd.DataFrame(
            [(x, y, round(p,4)) for ((x,y), p) in top_condicional],
            columns=["Se sair X", "Tende sair Y", "Probabilidade"]
        )

        st.dataframe(df_cond)
