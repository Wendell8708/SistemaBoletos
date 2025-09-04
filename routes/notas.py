from flask import Blueprint, jsonify, request
from config import get_db_connection

notas_bp = Blueprint("notas", __name__)

# Listar todas as notas fiscais
@notas_bp.route("/", methods=["GET"])
def get_notas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notas_fiscais")
    notas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(notas)

# Buscar nota por ID
@notas_bp.route("/<int:id>", methods=["GET"])
def get_nota(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notas_fiscais WHERE id = %s", (id,))
    nota = cursor.fetchone()
    cursor.close()
    conn.close()
    if nota:
        return jsonify(nota)
    return jsonify({"erro": "Nota fiscal não encontrada"}), 404

# Criar nota fiscal
@notas_bp.route("/", methods=["POST"])
def add_nota():
    novo = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notas_fiscais (cliente, descricao, valor_total, status)
        VALUES (%s, %s, %s, %s)
    """, (
        novo["cliente"],
        novo.get("descricao", ""),
        novo["valor_total"],
        novo.get("status", "emitida")
    ))
    conn.commit()
    novo["id"] = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify(novo), 201

# Atualizar nota fiscal
@notas_bp.route("/<int:id>", methods=["PUT"])
def update_nota(id):
    dados = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE notas_fiscais
        SET cliente = %s, descricao = %s, valor_total = %s, status = %s
        WHERE id = %s
    """, (
        dados["cliente"],
        dados.get("descricao", ""),
        dados["valor_total"],
        dados.get("status", "emitida"),
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Nota fiscal atualizada com sucesso"})

# Deletar nota fiscal
@notas_bp.route("/<int:id>", methods=["DELETE"])
def delete_nota(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notas_fiscais WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Nota fiscal deletada com sucesso"})
