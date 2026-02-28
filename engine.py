import pandas as pd
import random
from core.scoring import calcular_frequencia, calcular_atraso, calcular_score_dinamico
from core.genetic import evoluir
from core.montecarlo import validar_jogos, simular_jogo
from core.adaptativo import (
    calcular_performance,
    classificar_estado,
    salvar_estado,
    atualizar_peso_bayes,
)


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


def limpar_dataframe(df, universo):

    df = df.copy()

    # Converte tudo para string e limpa espaços
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    # Remove símbolos inválidos comuns
    df = df.replace(['-', '', 'nan', 'None'], pd.NA)

    # Converte para número de forma segura
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove linhas totalmente vazias
    df = df.dropna(how='all')

    # Converte para inteiro apenas valores válidos
    df = df.applymap(lambda x: int(x) if pd.notna(x) else None)

    # Remove números fora do universo
    df = df.applymap(lambda x: x if x in universo else None)

    df = df.dropna(how='all')

    return df


def executar_modelo(df, loteria):

    universo, tamanho_jogo = configurar_loteria(loteria)

    df = limpar_dataframe(df, universo)

    if df.empty:
        raise ValueError("Arquivo sem dados válidos após limpeza.")

    freq = calcular_frequencia(df)
    atraso = calcular_atraso(df, universo)

    if not freq:
        raise ValueError("Não foi possível calcular frequência.")

    score = calcular_score_dinamico(freq, atraso)

    jogos = evoluir(universo, tamanho_jogo, score)

    jogos_corrigidos = []

    for jogo in jogos:
        jogo = list(set([n for n in jogo if n in universo]))

        while len(jogo) < tamanho_jogo:
            novo = random.choice(universo)
            if novo not in jogo:
                jogo.append(novo)

        jogos_corrigidos.append(sorted(jogo[:tamanho_jogo]))

    jogos_validados = validar_jogos(jogos_corrigidos, universo, tamanho_jogo)

    scores_mc = [
        simular_jogo(j, universo, tamanho_jogo)
        for j in jogos_validados
    ]

    performance = calcular_performance(scores_mc)

    estado = classificar_estado(performance)
    salvar_estado(loteria, estado)

    atualizar_peso_bayes(loteria, "GA+MC", performance)

    return jogos_validados[:3], estado, performance
