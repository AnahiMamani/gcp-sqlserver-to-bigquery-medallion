from google_client import obter_texto_conexao_secret_manager
import pyodbc # Biblioteca para conectar em bancos via driver ODBC
import pandas
import warnings
warnings.filterwarnings('ignore')

def conectar_banco_sql_server(nome_do_banco):
    # Busca a base da conexão (servidor, user, senha) no Google Client
    string_base = obter_texto_conexao_secret_manager()
    string_completa = f"{string_base} Database={nome_do_banco}" # Adicionando o nome da Database
    return pyodbc.connect(string_completa)

def buscar_sqlServer_para_dataframe(objeto_conexao, comando_sql):
    return pandas.read_sql(comando_sql, objeto_conexao)