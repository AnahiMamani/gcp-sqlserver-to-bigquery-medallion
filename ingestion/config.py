import os

# Caminhos e IDs
GOOGLE_CREDENTIALS = r"C:\Users\AnahiMamani\github-repo\sqlserver-to-bigquery-medallion\gas-price-482120-4fb583586af6.json"
PROJECT_ID = "gas-price-482120"

# Mapeamento de Ingestão: (Banco Origem, Tabela Origem, DatasetDestino.TabelaDestino)
TABELAS_INGESTAO = [
    ("PRODUCTION", "producao_etanol_anidro_bep_2012_2018", "bronze.producao_etanol_anidro"),
    ("PRODUCTION", "producao_etanol_anidro_2019", "bronze.producao_etanol_anidro_2019"),
    ("PRICE", "precos_dolar", "bronze.fact_preco_dolar_mensal_raw"),
    ("PRICE", "precos_petroleo", "bronze.fact_preco_petroleo_mensal_raw"),
    ("PRICE", "precos_combustiveis_anp", "bronze.fact_precos_combustiveis_mensal_raw")
]