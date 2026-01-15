from google.cloud import secretmanager, bigquery
import config
import os

# Configura a variável de ambiente para que as bibliotecas do Google 
# encontrem o seu arquivo JSON de chave privada automaticamente.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CREDENTIALS

def obter_texto_conexao_secret_manager():
    """
    Busca a 'ConnectionString' (endereço, usuário e senha) guardada de forma 
    segura no Secret Manager do Google, para não deixar senhas expostas no código.
    """
    cliente_secret = secretmanager.SecretManagerServiceClient()
    caminho_secret = f"projects/596283452642/secrets/sql-server-connection/versions/latest"
    
    resposta = cliente_secret.access_secret_version(request={"name": caminho_secret})
    # O segredo vem em formato binário (bytes), por isso usamos .decode("UTF-8") para virar texto.
    return resposta.payload.data.decode("UTF-8")

def get_connection_bigquery():
    """Inicia o cliente oficial do BigQuery para enviar comandos SQL ou carregar dados."""
    return bigquery.Client(project=config.PROJECT_ID)

def baixar_tabela_dq_nuvem(cliente, tabela_destino):
    """
    Tenta baixar os dados que já estão no BigQuery. 
    Se a tabela não existir (ex: primeira vez rodando), ele retorna 'None'.
    """
    query_busca = f"SELECT * FROM `{config.PROJECT_ID}.{tabela_destino}`"
    try:
        # Transforma o resultado da consulta SQL do BigQuery direto em um DataFrame do Pandas.
        return cliente.query(query_busca).to_dataframe()
    except Exception:
        # Caso a tabela ainda não tenha sido criada, o erro é ignorado para o pipeline seguir.
        return None 

def inserir_dados_no_bigquery(cliente, dataframe, tabela_destino):
    """
    Pega um DataFrame do Pandas e o envia para o BigQuery.
    Usa o modo 'WRITE_APPEND', que significa: adicione ao final do que já existe.
    """
    if dataframe.empty: 
        return
        
    id_tabela = f"{config.PROJECT_ID}.{tabela_destino}"
    
    # Configura o carregamento: se a tabela já existir, ele apenas acrescenta (Append)
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    
    job = cliente.load_table_from_dataframe(dataframe, id_tabela, job_config=job_config) # Make an API request
    job.result() # Wait for the job to complete

def deletar_linhas_por_chave(cliente, tabela_destino, dataframe_deletar, lista_colunas_chave):
    """
    Executa comandos de DELETE cirúrgicos. 
    Para cada linha no DataFrame, ele gera um 'DELETE WHERE coluna1=x AND coluna2=y'.
    """
    if dataframe_deletar.empty: 
        return
        
    id_tabela = f"{config.PROJECT_ID}.{tabela_destino}"
    
    # Percorre linha por linha do que precisa ser removido
    #for indice, linha in-- mas aqui o indice não ajuda em nada então _ pois :P
    for _, linha in dataframe_deletar.iterrows():
        # Cria a parte do filtro: `ANO` = '2012' AND `ESTADO` = 'SP' ...
        condicoes_filtro = " AND ".join([f"`{col}` = '{linha[col]}'" for col in lista_colunas_chave])
        
        comando_sql = f"DELETE FROM `{id_tabela}` WHERE {condicoes_filtro}"
        
        # Envia o comando de deletar para o BigQuery
        cliente.query(comando_sql).result()