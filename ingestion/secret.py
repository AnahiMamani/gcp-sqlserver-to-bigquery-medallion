from google.cloud import secretmanager
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

def get_connection_string():
    client = secretmanager.SecretManagerServiceClient()
    
    project_id = os.getenv("GCP_PROJECT_ID")
    secret_id = os.getenv("SECRET_ID")
    
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name":name})
    payload = response.payload.data.decode("UTF-8")
    return payload