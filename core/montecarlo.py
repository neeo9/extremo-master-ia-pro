import random


def simular_jogo(jogo, universo, tamanho_jogo, simulacoes=2000):
    """
    Simula vários sorteios aleatórios
    e calcula média de acertos do jogo
    """
    total_acertos = 0

    for _ in range(simulacoes):
        sorteio = random.sample(universo, tamanho_jogo)
        acertos = len(set(jogo) & set(sorteio))
        total_acertos += acertos

    return total_acertos / simulacoes


def validar_jogos(jogos, universo, tamanho_jogo):
    """
    Retorna jogos ordenados pelo desempenho no Monte Carlo
    """
    avaliacao = []

    for jogo in jogos:
        media = simular_jogo(jogo, universo, tamanho_jogo)
        avaliacao.append((jogo, media))

    avaliacao.sort(key=lambda x: x[1], reverse=True)

    return [j[0] for j in avaliacao]
