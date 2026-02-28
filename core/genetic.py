import random


def gerar_populacao(universo, tamanho_jogo, tamanho_pop=300):
    return [random.sample(universo, tamanho_jogo) for _ in range(tamanho_pop)]


def fitness(jogo, score_dict):
    return sum(score_dict.get(n, 0) for n in jogo)


def selecionar(populacao, score_dict, elite=80):
    populacao.sort(key=lambda x: fitness(x, score_dict), reverse=True)
    return populacao[:elite]


def crossover(pai1, pai2, tamanho_jogo):
    corte = tamanho_jogo // 2
    filho = list(set(pai1[:corte] + pai2[corte:]))

    while len(filho) < tamanho_jogo:
        filho.append(random.choice(pai1))

    return filho[:tamanho_jogo]


def mutacao(jogo, universo, taxa=0.15):
    if random.random() < taxa:
        pos = random.randint(0, len(jogo)-1)
        novo = random.choice(universo)
        while novo in jogo:
            novo = random.choice(universo)
        jogo[pos] = novo
    return jogo


def evoluir(universo, tamanho_jogo, score_dict, geracoes=30):
    populacao = gerar_populacao(universo, tamanho_jogo)

    for _ in range(geracoes):
        elite = selecionar(populacao, score_dict)

        nova_pop = elite.copy()

        for i in range(len(elite)//2):
            pai1 = elite[i]
            pai2 = elite[-i-1]

            filho = crossover(pai1, pai2, tamanho_jogo)
            filho = mutacao(filho, universo)

            nova_pop.append(filho)

        populacao = nova_pop

    populacao.sort(key=lambda x: fitness(x, score_dict), reverse=True)

    return populacao[:3]
