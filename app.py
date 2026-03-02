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
# LIMPEZA ULTRA ROBUSTA
# ==============================

def limpar_dados(df):
    df = df.copy()

    # Garantir que tudo é string
    df = df.astype(str)

    # Remover espaços
    df = df.applymap(lambda x: x.strip())

    # Remover qualquer coisa que não seja número
    df = df.replace(r"[^\d]", "", regex=True)

    # Converter para número com segurança total
    df = df.apply(pd.to_numeric, errors="coerce")

    # Remover colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    # Remover linhas totalmente vazias
    df = df.dropna(axis=0, how="all")

    # Substituir NaN por 0
    df = df.fillna(0)

    return df

# ==============================
# GERADOR
# ==============================

def gerar_jogo_unico(total_range, quantidade):
    return sorted(random.sample(range(1, total_range + 1), quantidade))

# ==============================
# MOTOR
# ==============================

def executar_modelo(nome_loteria, df):
    config = CONFIG[nome_loteria]

    df = limpar_dados(df)

    jogos = []
    for _ in range(3):
        jogos.append(
            gerar_jogo_unico(config["range"], config["qtd"])
        )

    return jogos

# ==============================
# INTERFACE
# ==============================

st.title("🔥 EXTREMO MASTER IA PRO")

loteria = st.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofácil", "Quina", "Lotomania"]
)

arquivo = st.file_uploader("Envie o arquivo Excel com os resultados", type=["xlsx"])

if arquivo:
    try:
        # 🔥 AQUI ESTÁ A CORREÇÃO REAL
        df = pd.read_excel(arquivo, dtype=str)

        st.success("Arquivo carregado com sucesso!")

        if st.button("Gerar Palpites"):
            jogos = executar_modelo(loteria, df)

            st.subheader("🎯 Palpites Gerados:")
            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {', '.join(map(str, jogo))}")

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
