# FORCE REBUILD 01
import streamlit as st
import pandas as pd
import random
import re
from io import BytesIO

st.set_page_config(page_title="EXTREMO MASTER IA PRO", layout="wide")

CONFIG = {
    "Mega-Sena": {"range": 60, "qtd": 6},
    "Lotofácil": {"range": 25, "qtd": 15},
    "Quina": {"range": 80, "qtd": 5},
    "Lotomania": {"range": 100, "qtd": 50},
}

# ==============================
# LEITURA 100% SEGURA DO EXCEL
# ==============================

def ler_excel_seguro(arquivo):
    bytes_data = arquivo.read()
    buffer = BytesIO(bytes_data)

    # Lê sem inferência automática problemática
    df = pd.read_excel(
        buffer,
        engine="openpyxl",
        header=None,
        dtype=object
    )

    return df

# ==============================
# EXTRAÇÃO SEGURA DE NÚMEROS
# ==============================

def extrair_numeros_validos(df, limite):
    numeros = []

    for linha in df.values:
        for valor in linha:
            if valor is None:
                continue

            texto = str(valor)

            encontrados = re.findall(r"\d+", texto)

            for n in encontrados:
                num = int(n)
                if 1 <= num <= limite:
                    numeros.append(num)

    return numeros

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

    # Apenas extrai números válidos (não converte DataFrame)
    extrair_numeros_validos(df, config["range"])

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
        df = ler_excel_seguro(arquivo)

        st.success("Arquivo carregado com sucesso!")

        if st.button("Gerar Palpites"):
            jogos = executar_modelo(loteria, df)

            st.subheader("🎯 Palpites Gerados:")
            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {', '.join(map(str, jogo))}")

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
