from flask import Blueprint, jsonify, request
from config import get_db_connection

boletos_bp = Blueprint("boletos", __name__)

# Listar todos os boletos
@boletos_bp.route("/", methods=["GET"])
def get_boletos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.id, b.valor, b.vencimento, b.situação, b.comprovante, f.nome AS fornecedor
        FROM boletos b
        JOIN fornecedores f ON b.fornecedor_id = f.id
    """)
    boletos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(boletos)

# Buscar boleto por ID
@boletos_bp.route("/<int:id>", methods=["GET"])
def get_boleto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.id, b.valor, b.vencimento, b.situação, b.comprovante, f.nome AS fornecedor
        FROM boletos b
        JOIN fornecedores f ON b.fornecedor_id = f.id
        WHERE b.id = %s
    """, (id,))
    boleto = cursor.fetchone()
    cursor.close()
    conn.close()
    if boleto:
        return jsonify(boleto)
    return jsonify({"erro": "Boleto não encontrado"}), 404

# Criar boleto
@boletos_bp.route("/", methods=["POST"])
def add_boleto():
    novo = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO boletos (fornecedor_id, valor, vencimento, situação, comprovante)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        novo["fornecedor_id"],
        novo["valor"],
        novo["vencimento"],
        novo.get("situação", "pendente"),
        novo.get("comprovante")
    ))
    conn.commit()
    novo["id"] = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify(novo), 201

# Atualizar boleto
@boletos_bp.route("/<int:id>", methods=["PUT"])
def update_boleto(id):
    dados = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE boletos
        SET fornecedor_id = %s, valor = %s, vencimento = %s, situação = %s, comprovante = %s
        WHERE id = %s
    """, (
        dados["fornecedor_id"],
        dados["valor"],
        dados["vencimento"],
        dados["situação"],
        dados.get("comprovante"),
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Boleto atualizado com sucesso"})

# Deletar boleto
@boletos_bp.route("/<int:id>", methods=["DELETE"])
def delete_boleto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM boletos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Boleto deletado com sucesso"})

# Consultar boletos pendentes
@boletos_bp.route("/pendentes", methods=["GET"])
def get_boletos_pendentes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM boletos WHERE situação = 'pendente'")
    boletos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(boletos)

# Consultar boletos vencidos
@boletos_bp.route("/vencidos", methods=["GET"])
def get_boletos_vencidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM boletos WHERE situação = 'Vencido'")
    boletos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(boletos)

# Boletos próximos a vencer (7 dias)
@boletos_bp.route("/proximos", methods=["GET"])
def get_boletos_proximos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM boletos
        WHERE vencimento BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY
    """)
    boletos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(boletos)