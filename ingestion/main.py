from database import conectar_banco, buscar_dados
from dotenv import load_dotenv
import os

load_dotenv() #ler sobre

def pipeline_producao():
    # Agora você pode alternar entre bancos facilmente!
    # db_name = input("Insira o nome do banco: ") 
    db_name = os.getenv("DATABASE")
    
    print(f"Iniciando processo para o banco: {db_name}")
    conn = conectar_banco(db_name)
    
    try:
        dados = buscar_dados(conn, "SELECT TOP 10 * FROM producao_etanol_anidro_bep_2012_2018")
        print(f"Processados {dados} registros.")
    finally:
        conn.close()

# Esse if significa que se eu rodar diretamente este arquivo, então ai o pipeline_producao()
# ira ser executado, caso eu importe essa arquivo para outro arquivo o que esta dentro desse
# if aqui embaixo, não sera executado....
if __name__ == "__main__":
    pipeline_producao()