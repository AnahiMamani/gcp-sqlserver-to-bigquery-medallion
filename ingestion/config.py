import os

GOOGLE_CREDENTIALS = r"C:\Users\AnahiMamani\github-repo\sqlserver-to-bigquery-medallion\gas-price-482120-4fb583586af6.json"
PROJECT_ID = "gas-price-482120"

# Mapeamento: (Banco, Tabela_SQL, Tabela_BQ, LISTA_CHAVES_NATURAIS)
TABELAS_INGESTAO = [
    ("PRODUCTION", "producao_etanol_anidro_bep_2019", "bronze.producao_etanol_anidro_bep_2019", ["ANO", "ESTADO", "REGIAO"])
]