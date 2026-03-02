import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="wide")

# ==============================
# CONFIGURAÇÃO DAS LOTERIAS
# ==============================

CONFIG = {
    "Mega-Sena": {"range": 60, "qtd": 6},
    "Lotofácil": {"range": 25, "qtd": 15},
    "Quina": {"range": 80, "qtd": 5},
    "Lotomania": {"range": 100, "qtd": 50},
}

# ==============================
# LIMPEZA ROBUSTA DO EXCEL
# ==============================

def limpar_dados(df):
    df = df.copy()

    # Converte tudo para string e remove espaços
    df = df.applymap(lambda x: str(x).strip())

    # Remove qualquer caractere que não seja número
    df = df.replace(r"[^\d]", "", regex=True)

    # Converte para numérico com segurança
    df = df.apply(pd.to_numeric, errors="coerce")

    # Remove colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    # Remove linhas totalmente vazias
    df = df.dropna(axis=0, how="all")

    # Preenche NaN restantes com 0
    df = df.fillna(0).astype(int)

    return df

# ==============================
# GERADOR DE JOGO ÚNICO
# ==============================

def gerar_jogo_unico(total_range, quantidade):
    numeros = set()

    while len(numeros) < quantidade:
        numeros.add(random.randint(1, total_range))

    return sorted(list(numeros))

# ==============================
# MOTOR PRINCIPAL
# ==============================

def executar_modelo(nome_loteria, df):
    config = CONFIG[nome_loteria]

    # Limpa os dados (principalmente importante p/ Lotomania)
    df = limpar_dados(df)

    jogos = []

    for _ in range(3):
        jogo = gerar_jogo_unico(config["range"], config["qtd"])
        jogos.append(jogo)

    return jogos

# ==============================
# INTERFACE STREAMLIT
# ==============================

st.title("🔥 EXTREMO MASTER IA PRO")

loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofácil", "Quina", "Lotomania"]
)

arquivo = st.file_uploader("Envie o arquivo Excel com os resultados", type=["xlsx"])

if arquivo:
    try:
        df = pd.read_excel(arquivo)
        st.success("Arquivo carregado com sucesso!")

        if st.button("Gerar Palpites"):
            jogos = executar_modelo(loteria, df)

            st.subheader("🎯 Palpites Gerados:")
            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {', '.join(map(str, jogo))}")

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
