from database.db import conectar
from datetime import datetime


def calcular_performance(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)


def classificar_estado(performance):
    if performance >= 0.75:
        return "🟢 Estável"
    elif performance >= 0.55:
        return "🟡 Atenção"
    else:
        return "🔴 Crítico"


def salvar_estado(loteria, estado):
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    INSERT INTO estados_modelo (loteria, estado, data_estado)
    VALUES (?, ?, ?)
    """, (loteria, estado, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def atualizar_peso_bayes(loteria, tecnica, taxa_acerto):
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    SELECT peso FROM pesos_modelo
    WHERE loteria = ? AND tecnica = ?
    """, (loteria, tecnica))

    resultado = c.fetchone()

    if resultado:
        peso_antigo = resultado[0]
        novo_peso = peso_antigo * (1 + taxa_acerto)
        c.execute("""
        UPDATE pesos_modelo
        SET peso = ?
        WHERE loteria = ? AND tecnica = ?
        """, (novo_peso, loteria, tecnica))
    else:
        novo_peso = 1 + taxa_acerto
        c.execute("""
        INSERT INTO pesos_modelo (loteria, tecnica, peso)
        VALUES (?, ?, ?)
        """, (loteria, tecnica, novo_peso))

    conn.commit()
    conn.close()
