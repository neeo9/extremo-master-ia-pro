import json
import os
import numpy as np


ESTADO_FILE = "estado_modelo.json"


def calcular_performance(scores):

    if not scores or len(scores) == 0:
        return 0

    scores = [s for s in scores if s is not None]

    if len(scores) == 0:
        return 0

    return float(np.mean(scores))


def classificar_estado(performance):

    if performance == 0:
        return "FRIO"

    elif performance < 0.3:
        return "INSTAVEL"

    else:
        return "FORTE"


def salvar_estado(loteria, estado):

    dados = {}

    if os.path.exists(ESTADO_FILE):
        with open(ESTADO_FILE, "r") as f:
            try:
                dados = json.load(f)
            except:
                dados = {}

    dados[loteria] = estado

    with open(ESTADO_FILE, "w") as f:
        json.dump(dados, f)


def atualizar_peso_bayes(loteria, modelo, performance):

    # Proteção total contra erro
    if performance is None:
        return

    return
