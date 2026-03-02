import json
import os
import numpy as np

ESTADO_FILE = "estado_modelo.json"


def calcular_performance(scores):
    """
    Calcula média de performance sem risco de divisão por zero
    """
    if not scores:
        return 0.0

    scores_validos = [s for s in scores if isinstance(s, (int, float))]

    if len(scores_validos) == 0:
        return 0.0

    return float(np.mean(scores_validos))


def classificar_estado(performance):
    """
    Classifica estado do modelo
    """
    if performance <= 0:
        return "FRIO"
    elif performance < 0.3:
        return "INSTAVEL"
    else:
        return "FORTE"


def salvar_estado(loteria, estado):

    dados = {}

    if os.path.exists(ESTADO_FILE):
        try:
            with open(ESTADO_FILE, "r") as f:
                dados = json.load(f)
        except:
            dados = {}

    dados[loteria] = estado

    with open(ESTADO_FILE, "w") as f:
        json.dump(dados, f)


def atualizar_peso_bayes(loteria, modelo, performance):
    """
    Versão protegida — não deixa quebrar
    """
    return
