from flask import Blueprint, jsonify
from config import get_db_connection

relatorios_bp = Blueprint("relatorios", __name__)

# ----------------- BOLETOS POR SITUAÇÃO -----------------
@relatorios_bp.route("/boletos/situacao", methods=["GET"])
def boletos_por_situacao():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT situação, COUNT(*) AS quantidade
        FROM boletos
        GROUP BY situação
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

# ----------------- BOLETOS A VENCER EM 7 DIAS -----------------
@relatorios_bp.route("/boletos/proximos", methods=["GET"])
def boletos_proximos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.id, b.valor, b.vencimento, f.nome AS fornecedor
        FROM boletos b
        JOIN fornecedores f ON b.fornecedor_id = f.id
        WHERE b.vencimento BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

# ----------------- MAIOR VALOR DE BOLETOS POR FORNECEDOR -----------------
@relatorios_bp.route("/boletos/maior_valor", methods=["GET"])
def boletos_maior_valor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.nome, MAX(b.valor) AS maior_valor
        FROM fornecedores f
        JOIN boletos b ON f.id = b.fornecedor_id
        GROUP BY f.id
        ORDER BY maior_valor DESC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

# ----------------- ORÇAMENTOS POR STATUS -----------------
@relatorios_bp.route("/orcamentos/status", methods=["GET"])
def orcamentos_por_status():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT status, COUNT(*) AS quantidade
        FROM orcamentos
        GROUP BY status
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

# ----------------- NOTAS EMITIDAS POR PERÍODO -----------------
@relatorios_bp.route("/notas/periodo", methods=["GET"])
def notas_por_periodo():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Exemplo: notas emitidas nos últimos 30 dias
    cursor.execute("""
        SELECT *
        FROM notas_fiscais
        WHERE data_emissao BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

# ----------------- RESUMO FINANCEIRO GERAL -----------------
@relatorios_bp.route("/financeiro/resumo", methods=["GET"])
def resumo_financeiro():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total boletos pendentes
    cursor.execute("SELECT SUM(valor) AS total_pendentes FROM boletos WHERE situação='pendente'")
    total_pendentes = cursor.fetchone()["total_pendentes"] or 0

    # Total boletos pagos
    cursor.execute("SELECT SUM(valor) AS total_pagos FROM boletos WHERE situação='Pago'")
    total_pagos = cursor.fetchone()["total_pagos"] or 0

    # Total orçamentos abertos
    cursor.execute("SELECT SUM(valor_total) AS total_orcamentos_abertos FROM orcamentos WHERE status='aberto'")
    total_orcamentos_abertos = cursor.fetchone()["total_orcamentos_abertos"] or 0

    # Total notas emitidas
    cursor.execute("SELECT SUM(valor_total) AS total_notas_emitidas FROM notas_fiscais WHERE status='emitida'")
    total_notas_emitidas = cursor.fetchone()["total_notas_emitidas"] or 0

    cursor.close()
    conn.close()

    resumo = {
        "boletos": {
            "pendentes": float(total_pendentes),
            "pagos": float(total_pagos)
        },
        "orcamentos_abertos": float(total_orcamentos_abertos),
        "notas_emitidas": float(total_notas_emitidas)
    }
    return jsonify(resumo)
