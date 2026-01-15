GOOGLE_CREDENTIALS = r"C:\Users\AnahiMamani\github-repo\sqlserver-to-bigquery-medallion\gas-price-482120-4fb583586af6.json"
PROJECT_ID = "gas-price-482120"

# Mapeamento: (Banco, Tabela_SQL, Tabela_BQ, LISTA_CHAVES_NATURAIS)
TABELAS_INGESTAO = [
    ("PRODUCTION", "producao_etanol_anidro_bep_2019", "ds_gas_price_bronze.producao_etanol_anidro_bep_2019", ["ANO", "ESTADO", "REGIAO"]),
    ("PRODUCTION", "producao_etanol_anidro_bep_2012_2018", "ds_gas_price_bronze.producao_etanol_anidro_bep_2012_2018", ["ANO", "ESTADO", "REGIAO"]),

    ("PRICE", "preco_dolar_mensal", "ds_gas_price_bronze.preco_dolar_mensal", ["Data"]),
    ("PRICE", "preco_petroleo_mensal", "ds_gas_price_bronze.preco_petroleo_mensal", ["Data"]),
    ("PRICE", "preco_gasolina_mensal_2001_2012", "ds_gas_price_bronze.preco_gasolina_mensal_2001_2012", ["column1"]),
    ("PRICE", "preco_gasolina_mensal_2013_2019", "ds_gas_price_bronze.preco_gasolina_mensal_2013_2019", ["column1"]),
]