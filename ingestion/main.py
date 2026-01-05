import pyodbc 
# Biblioteca que permite se conectar com bancos que utilizam padrão ODBC como o SQL Server

dados_conexão = (
    "Driver={ODBC Driver 17 for SQL Server};" # Motor que o python vai usar
    "Server=maquina;" # The conputer name where the database is located
    "Database=dbManga;" # Database name
    "Trusted_Connection=yes;" # Tell SQl Server to use the windows user to authenticate
) # String de conesão que possue os dados necessarios para ter uma conesão bem sucedida


try:
    conexao = pyodbc.connect(dados_conexão) # Create the connection
    print("Conexão bem sucedida")
    
    # Cursor é um carteiro que leva os comandos sql para o banco e retorna com os dados
    cursor = conexao.cursor() 
    cursor.execute("SELECT * FROM mangaVendas")
    
    # O execute prepara todos os dados no servidor. Ja o fetchone traz o primeiro dado 
    row = cursor.fetchone() # or fetchall() 
    print(row)

except Exception as e:
    print(f"Erro ao conectar: {e}")