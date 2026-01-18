from datetime import datetime
import google_client
import database
import config
import pandas as pd

def executar_pipeline_ingestao_bronze():
    # Inicializa o cliente do BigQuery
    cliente_bigquery = google_client.get_connection_bigquery()

    # Percorre cada tabela configurada no arquivo config.py
    for banco_sql, tabela_fonte, tabela_destino, colunas_chave in config.TABELAS_INGESTAO:
        
        # Abre conexão com o SQL Server local
        conexao_sql = database.conectar_banco_sql_server(banco_sql)
        
        try:
            # 1. EXTRAÇÃO: Busca os dados da Origem (SQL) e do Destino (Cloud)
            # .astype(str) garante que a comparação seja feita texto com texto
            dados_origem_sql = database.buscar_sqlServer_para_dataframe(conexao_sql, f'SELECT * FROM {tabela_fonte}').astype(str)
            dados_atuais_nuvem = google_client.baixar_tabela_dq_nuvem(cliente_bigquery, tabela_destino)
            
            # 2. CARGA INICIAL: Se a tabela na nuvem não existir, envia tudo
            if dados_atuais_nuvem is None or dados_atuais_nuvem.empty:
                print(f"Primeira vez: Enviando todos os dados para {tabela_destino}...")
                dados_origem_sql['ingestion_timestamp'] = datetime.now().isoformat()
                google_client.inserir_dados_no_bigquery(cliente_bigquery, dados_origem_sql, tabela_destino)
            
            else:
                dados_atuais_nuvem = dados_atuais_nuvem.astype(str)
                
                # 3. IDENTIFICAÇÃO DE DELETADOS (Estão na Nuvem, mas sumiram do SQL)
                # O merge 'left' com indicator identifica linhas que só existem no lado esquerdo (Nuvem)
                comparar_exclusao = dados_atuais_nuvem.merge(dados_origem_sql[colunas_chave], on=colunas_chave, how='left', indicator=True)
                registros_deletados = comparar_exclusao[comparar_exclusao['_merge'] == 'left_only'].drop(columns=['_merge'])

                # 4. IDENTIFICAÇÃO DE NOVOS (Estão no SQL, mas não chegaram na Nuvem ainda)
                comparar_novos = dados_origem_sql.merge(dados_atuais_nuvem[colunas_chave], on=colunas_chave, how='left', indicator=True)
                registros_novos = comparar_novos[comparar_novos['_merge'] == 'left_only'].drop(columns=['_merge'])

                # 5. IDENTIFICAÇÃO DE ALTERADOS (Existem nos dois, mas algum valor mudou)
                # 'inner' merge traz apenas o que tem nos dois para compararmos as colunas
                # Dados_origem_sql - Left     dados_atuais_nuvem - Ritgh    on=colunas comparadas  how- inner(pega dos dois lado) 
                registros_comuns = dados_origem_sql.merge(dados_atuais_nuvem, on=colunas_chave, how='inner', suffixes=('', '_nuvem'))
                # List Comprehensions
                colunas_dados = [c for c in dados_origem_sql.columns if c not in colunas_chave and c != 'ingestion_timestamp'] # Sai colunas -time -chaves

                foi_alterado = False
                for col in colunas_dados:
                # Conceito de acumulação logica, comparando o valor logico recebido antes com o de agora.
                # Lista de true e false incremental           é diferente de?      me devolve uma coluna de decisão true ou false, ele ve cada linha.
                    foi_alterado |= (registros_comuns[col] != registros_comuns[col + '_nuvem'])
                # filtro com base nos true/false achados, ficamos so com os true  ai no procximo [] deletamos as colunas que nao sao iguais as de dados_origen_sql.collums
                registros_alterados = registros_comuns[foi_alterado][dados_origem_sql.columns]
                
                # 6. SINCRONIZAÇÃO (Ação cirúrgica no BigQuery)
                # Passo A: Deletar da Nuvem o que foi apagado no SQL ou o que mudou (para atualizar)
                lista_para_remover = pd.concat([registros_deletados, registros_alterados])
                if not lista_para_remover.empty:
                    print(f"Limpando {len(lista_para_remover)} registros desatualizados...")
                    google_client.deletar_linhas_por_chave(cliente_bigquery, tabela_destino, lista_para_remover, colunas_chave)

                # Passo B: Inserir o que é novo e a versão atualizada dos alterados
                lista_para_inserir = pd.concat([registros_novos, registros_alterados])
                if not lista_para_inserir.empty:
                    print(f"Sincronizando {len(lista_para_inserir)} registros novos/atualizados...")
                    lista_para_inserir['ingestion_timestamp'] = datetime.now().isoformat()
                    google_client.inserir_dados_no_bigquery(cliente_bigquery, lista_para_inserir, tabela_destino)

            print(f'✅ Pipeline concluída para: {tabela_fonte}')
            
        except Exception as erro:
            print(f'❌ Falha na sincronização de {tabela_fonte}: {erro}')
        finally:
            conexao_sql.close()

if __name__ == "__main__":
    executar_pipeline_ingestao_bronze()