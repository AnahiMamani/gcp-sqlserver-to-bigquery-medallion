from database import conectar_banco, buscar_dados
import os

def pipeline_producao():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\AnahiMamani\github-repo\sqlserver-to-bigquery-medallion\gas-price-482120-4fb583586af6.json"

    # db_name = input("Insira o nome do banco: ")  
    db_name = "PRODUCTION"
    
    print(f"Iniciando processo para o banco: {db_name}")
    conn = conectar_banco(db_name)
    
    try:
        dados = buscar_dados(conn, "SELECT * FROM producao_etanol_anidro_bep_2012_2018")
        print(f"Processados {len(dados)} registros.")
    finally:
        conn.close()

# Esse if significa que se eu rodar diretamente este arquivo, então ai o pipeline_producao()
# ira ser executado, caso eu importe essa arquivo para outro arquivo o que esta dentro desse
# if aqui embaixo, não sera executado....
if __name__ == "__main__":
    pipeline_producao()