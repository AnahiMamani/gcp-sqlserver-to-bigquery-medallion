from datetime import datetime
import google_client
import database
import config
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\AnahiMamani\github-repo\sqlserver-to-bigquery-medallion\gas-price-482120-4fb583586af6.json"

def pipeline_bronze():

    client_bq = google_client.get_connection_bigquery()

    for db_nome, tab_origem, tab_destino in config.TABELAS_INGESTAO:
        conn = database.conectar_banco(db_nome)

        try:
            query = f'SELECT * FROM {tab_origem}'
            df = database.buscar_dados(conn, query)
            
            df = df.astype(str)
            df['source_file'] = tab_origem
            df['ingestion_timestamp'] = datetime.now()

            google_client.job(client_bq, df, tab_destino)
            print('SUCESSO')
        except:
            print('ERRO')
        finally:
            conn.close()

if __name__ == "__main__":
    pipeline_bronze()