from google_client import get_connection_string
import pyodbc
import pandas
# import warnings
# warnings.filterwarnings('ignore')

def conectar_banco(nome_database):
    base_final = get_connection_string()
    string_final = f"{base_final} Database={nome_database}"
    return pyodbc.connect(string_final)

def buscar_dados(conexao, query):
    return pandas.read_sql(query, conexao)
