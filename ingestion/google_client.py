from google.cloud import secretmanager
from google.cloud import bigquery
import config
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\AnahiMamani\github-repo\sqlserver-to-bigquery-medallion\gas-price-482120-4fb583586af6.json"

# Secret Manager
def get_connection_string():
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/596283452642/secrets/sql-server-connection/versions/latest"
    response = client.access_secret_version(request={"name":name})
    payload = response.payload.data.decode("UTF-8")
    return payload

# BIg Query
def get_connection_bigquery():
    return bigquery.Client(project=config.PROJECT_ID)

def job(client, df, tab_destino,):
    table_id = f"{config.PROJECT_ID}.{tab_destino}"
    
    job_config = bigquery.LoadJobConfig(
        # 'WRITE_TRUNCATE' equivale ao if_exists='replace'
        write_disposition="WRITE_TRUNCATE", 
    )

    print(f"Enviando {len(df)} registros para {table_id}...")
    
    # O cliente oficial carrega o dataframe
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    
    # Espera o processo terminar
    return job.result() 