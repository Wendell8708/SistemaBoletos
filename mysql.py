import mysql.connector
from mysql.connector import Error


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Endereço do servidor MySQL
            user="root",  # Seu usuário do MySQL
            password="root",  # Sua senha do MySQL
            database="sistema_boletos"  # Nome do banco de dados
        )

        # Verifica se a conexão foi bem-sucedida
        if connection.is_connected():
            print("Conexão bem-sucedida com o MySQL")
        return connection
    except Error as e:
        print(f"Erro ao conectar com o MySQL: {e}")
        return None