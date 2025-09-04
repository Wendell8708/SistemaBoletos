from flask import Flask, jsonify, request
from config import get_db_connection

app = Flask(__name__)

# Rota para listar todos os fornecedores
@app.route('/fornecedores', methods=['GET'])
def get_fornecedores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fornecedores")
    fornecedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(fornecedores)

# Rota para adicionar um novo fornecedor
@app.route('/fornecedores', methods=['POST'])
def add_fornecedor():
    novo_fornecedor = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fornecedores (nome, cnpj, contato) VALUES (%s, %s, %s)",
                   (novo_fornecedor['nome'], novo_fornecedor['cnpj'], novo_fornecedor['contato']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(novo_fornecedor), 201

if __name__ == '__main__':
    app.run(debug=True)