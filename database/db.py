import sqlite3
import os
from datetime import datetime

DB_PATH = "data/loterias.db"

def conectar():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        loteria TEXT,
        concurso INTEGER,
        dezenas TEXT,
        data_importacao TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS pesos_modelo (
        loteria TEXT,
        tecnica TEXT,
        peso REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS performance (
        loteria TEXT,
        media REAL,
        ultima_atualizacao TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS estados_modelo (
        loteria TEXT,
        estado TEXT,
        data_estado TEXT
    )
    """)

    conn.commit()
    conn.close()


def salvar_resultado(loteria, concurso, dezenas):
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    INSERT INTO resultados (loteria, concurso, dezenas, data_importacao)
    VALUES (?, ?, ?, ?)
    """, (loteria, concurso, str(dezenas), datetime.now().isoformat()))

    conn.commit()
    conn.close()
