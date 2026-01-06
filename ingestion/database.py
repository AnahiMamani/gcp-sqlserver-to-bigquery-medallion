from secret import get_connection_string
import pyodbc

def conectar_banco(nome_database):
    base_final = get_connection_string()
    string_final = f"{base_final} Database={nome_database}"
    return pyodbc.connect(string_final)

def buscar_dados(conexao, query):
    cursor = conexao.cursor()
    cursor.execute(query)
    return cursor.fetchall()

print("veja que como nao temos o __main__ aqui, quandop eu importo pra main este arquivo database.py, vc pode ver este print\n Se este print estivesse em um if __name__ isso não seria visivel")