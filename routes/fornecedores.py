from flask import Blueprint, jsonify, request
from config import get_db_connection

fornecedores_bp = Blueprint("fornecedores", __name__)

# Listar fornecedores
@fornecedores_bp.route("/", methods=["GET"])
def get_fornecedores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fornecedores")
    fornecedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(fornecedores)

# Buscar fornecedor por ID
@fornecedores_bp.route("/<int:id>", methods=["GET"])
def get_fornecedor(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fornecedores WHERE id = %s", (id,))
    fornecedor = cursor.fetchone()
    cursor.close()
    conn.close()
    if fornecedor:
        return jsonify(fornecedor)
    return jsonify({"erro": "Fornecedor não encontrado"}), 404

# Criar fornecedor
@fornecedores_bp.route("/", methods=["POST"])
def add_fornecedor():
    novo = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fornecedores (nome, cnpj, contato) VALUES (%s, %s, %s)",
        (novo["nome"], novo["cnpj"], novo["contato"])
    )
    conn.commit()
    novo["id"] = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify(novo), 201

# Atualizar fornecedor
@fornecedores_bp.route("/<int:id>", methods=["PUT"])
def update_fornecedor(id):
    dados = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE fornecedores SET nome = %s, cnpj = %s, contato = %s WHERE id = %s
    """, (dados["nome"], dados["cnpj"], dados["contato"], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Fornecedor atualizado com sucesso"})

# Deletar fornecedor
@fornecedores_bp.route("/<int:id>", methods=["DELETE"])
def delete_fornecedor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fornecedores WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Fornecedor deletado com sucesso"})