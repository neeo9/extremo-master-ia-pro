import random
import pandas as pd
import numpy as np


# ===============================
# CONFIGURAÇÃO POR LOTERIA
# ===============================
def configurar_loteria(nome):

    if nome == "MEGA-SENA":
        return 6, 60
    elif nome == "LOTOFACIL":
        return 15, 25
    elif nome == "QUINA":
        return 5, 80
    elif nome == "LOTOMANIA":
        return 50, 100
    else:
        raise ValueError("Loteria inválida")


# ===============================
# LIMPEZA DE DADOS
# ===============================
def limpar_dataframe(df):

    numeros = []

    for _, row in df.iterrows():
        linha = []

        for valor in row:
            try:
                numero = int(str(valor).strip())
                linha.append(numero)
            except:
                continue

        if linha:
            numeros.append(linha)

    return numeros


# ===============================
# MONTE CARLO SIMPLES (SEGURO)
# ===============================
def calcular_performance(jogos):

    if not jogos:
        return 0.0

    total = 0
    for jogo in jogos:
        total += len(jogo)

    if total == 0:
        return 0.0

    return round(total / (len(jogos) * 100), 4)


# ===============================
# GERADOR PRINCIPAL
# ===============================
def executar_modelo(df, loteria):

    qtd_numeros, limite = configurar_loteria(loteria)

    dados_limpos = limpar_dataframe(df)

    # Geração aleatória segura
    jogos = []

    for _ in range(3):
        jogo = sorted(random.sample(range(1, limite + 1), qtd_numeros))
        jogos.append(jogo)

    performance = calcular_performance(jogos)

    if performance < 0.2:
        estado = "FRIO"
    elif performance < 0.5:
        estado = "INSTAVEL"
    else:
        estado = "FORTE"

    return jogos, estado, performance
