import pyodbc
import pandas as pd

# Lê os dados do Excel
dados = pd.read_json('dados_json2.json')


def conecta_ao_banco(driver='SQL Server', server='SAMUEL\\MSSQLSERVER01', database='Dados_scraping', trusted_connection="yes"):
    string_conexao = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};"
    conexao = pyodbc.connect(string_conexao)
    cursor = conexao.cursor()
    return conexao, cursor

try:
    conexao, cursor = conecta_ao_banco()
    print("Conexão estabelecida!")

    # Monta os nomes das colunas para a query
    nomes_colunas = ", ".join(f"[{col}]" for col in dados.columns)
    
    # Gera os placeholders para cada valor de coluna
    placeholders = ", ".join("?" for _ in dados.columns)

    # Insere os dados do DataFrame nas colunas existentes da tabela
    for _, row in dados.iterrows():
        # Aqui estamos pegando os valores da linha e substituindo qualquer NaN por None
        valores = tuple(row[col] if pd.notna(row[col]) else None for col in dados.columns)
        
        # Monta a query de inserção
        query = f"INSERT INTO ACOES ({nomes_colunas}) VALUES ({placeholders})"
        
        # Executa a query passando os valores da linha
        cursor.execute(query, valores)

    # Confirma as alterações no banco
    conexao.commit()
    print("Dados inseridos com sucesso!")

except Exception as e:
    print("Erro:", e)