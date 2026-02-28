import pandas as pd
from core.scoring import calcular_frequencia, calcular_atraso, calcular_score_dinamico
from core.genetic import evoluir
from core.montecarlo import validar_jogos, simular_jogo
from core.adaptativo import calcular_performance, classificar_estado, salvar_estado, atualizar_peso_bayes


def configurar_loteria(loteria):

    if loteria == "MEGA-SENA":
        return list(range(1, 61)), 6

    elif loteria == "LOTOFACIL":
        return list(range(1, 26)), 15

    elif loteria == "QUINA":
        return list(range(1, 81)), 5

    elif loteria == "LOTOMANIA":
        return list(range(0, 100)), 20

    else:
        raise ValueError("Loteria inválida")


def executar_modelo(df, loteria):

    universo, tamanho_jogo = configurar_loteria(loteria)

    # Limpa possíveis colunas extras
    df = df.select_dtypes(include=['int64', 'float64'])
    df = df.dropna()

    freq = calcular_frequencia(df)
    atraso = calcular_atraso(df, universo)
    score = calcular_score_dinamico(freq, atraso)

    # Algoritmo Genético
    jogos = evoluir(universo, tamanho_jogo, score)

    # Monte Carlo validação
    jogos_validados = validar_jogos(jogos, universo, tamanho_jogo)

    # Calcular performance
    scores_mc = [simular_jogo(j, universo, tamanho_jogo) for j in jogos_validados]
    performance = calcular_performance(scores_mc)

    # Estado adaptativo
    estado = classificar_estado(performance)
    salvar_estado(loteria, estado)

    # Atualiza peso fictício da técnica GA baseado na performance
    atualizar_peso_bayes(loteria, "GA+MC", performance)

    return jogos_validados[:3], estado, performance
