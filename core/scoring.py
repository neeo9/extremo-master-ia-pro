import numpy as np
import pandas as pd


def calcular_frequencia(df):
    """
    Conta quantas vezes cada dezena apareceu
    """
    if df.empty:
        return {}

    return df.stack().value_counts().to_dict()


def calcular_atraso(df, universo):
    """
    Calcula o atraso de cada dezena
    """
    atraso = {}

    if df.empty:
        return {n: 0 for n in universo}

    for dez in universo:
        posicoes = np.where(df.values == dez)

        if len(posicoes[0]) > 0:
            ultima_ocorrencia = posicoes[0].max()
            atraso[dez] = len(df) - ultima_ocorrencia
        else:
            atraso[dez] = len(df)

    return atraso


def calcular_score_dinamico(freq, atraso):
    """
    Combina frequência e atraso em um score único
    """

    score = {}

    if not freq:
        return {n: 0 for n in atraso.keys()}

    max_freq = max(freq.values()) if max(freq.values()) != 0 else 1
    max_atraso = max(atraso.values()) if max(atraso.values()) != 0 else 1

    for dez in atraso.keys():
        f = freq.get(dez, 0) / max_freq
        a = atraso.get(dez, 0) / max_atraso
        score[dez] = (0.6 * f) + (0.4 * a)

    return score
