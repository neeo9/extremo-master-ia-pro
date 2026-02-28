def executar_modelo(df, loteria):

    universo, tamanho_jogo = configurar_loteria(loteria)

    # Limpa apenas colunas numéricas
    df = df.select_dtypes(include=['int64', 'float64'])
    df = df.dropna()

    # Converte para inteiro
    df = df.astype(int)

    freq = calcular_frequencia(df)
    atraso = calcular_atraso(df, universo)
    score = calcular_score_dinamico(freq, atraso)

    jogos = evoluir(universo, tamanho_jogo, score)

    # Garante jogos válidos
    jogos = [
        sorted(list(set([n for n in jogo if n in universo])))[:tamanho_jogo]
        for jogo in jogos
    ]

    jogos_validados = validar_jogos(jogos, universo, tamanho_jogo)

    scores_mc = [simular_jogo(j, universo, tamanho_jogo) for j in jogos_validados]
    performance = calcular_performance(scores_mc)

    estado = classificar_estado(performance)
    salvar_estado(loteria, estado)

    atualizar_peso_bayes(loteria, "GA+MC", performance)

    return jogos_validados[:3], estado, performance
