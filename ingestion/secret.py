from google.cloud import secretmanager

def get_connection_string():
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/596283452642/secrets/sql-server-connection/versions/latest"
    response = client.access_secret_version(request={"name":name})
    payload = response.payload.data.decode("UTF-8")
    return payload
