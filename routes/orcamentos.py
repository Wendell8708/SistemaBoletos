from flask import Blueprint, jsonify, request
from config import get_db_connection

orcamentos_bp = Blueprint("orcamentos", __name__)

# Listar todos os orçamentos
@orcamentos_bp.route("/", methods=["GET"])
def get_orcamentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orcamentos")
    orcamentos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orcamentos)

# Buscar orçamento por ID
@orcamentos_bp.route("/<int:id>", methods=["GET"])
def get_orcamento(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orcamentos WHERE id = %s", (id,))
    orcamento = cursor.fetchone()
    cursor.close()
    conn.close()
    if orcamento:
        return jsonify(orcamento)
    return jsonify({"erro": "Orçamento não encontrado"}), 404

# Criar orçamento
@orcamentos_bp.route("/", methods=["POST"])
def add_orcamento():
    novo = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orcamentos (cliente, descricao, valor_total, status)
        VALUES (%s, %s, %s, %s)
    """, (
        novo["cliente"],
        novo.get("descricao", ""),
        novo["valor_total"],
        novo.get("status", "aberto")
    ))
    conn.commit()
    novo["id"] = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify(novo), 201

# Atualizar orçamento
@orcamentos_bp.route("/<int:id>", methods=["PUT"])
def update_orcamento(id):
    dados = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE orcamentos
        SET cliente = %s, descricao = %s, valor_total = %s, status = %s
        WHERE id = %s
    """, (
        dados["cliente"],
        dados.get("descricao", ""),
        dados["valor_total"],
        dados.get("status", "aberto"),
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Orçamento atualizado com sucesso"})

# Deletar orçamento
@orcamentos_bp.route("/<int:id>", methods=["DELETE"])
def delete_orcamento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orcamentos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Orçamento deletado com sucesso"})
