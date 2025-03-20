import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Lendo os tickers do arquivo
with open("acoes.txt", "r") as fundamentus_file:
    lista_acoes = fundamentus_file.read().split()

# Definindo o cabeçalho para evitar bloqueios
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Lista para armazenar os dados de cada ação
lista_dfs = []

# Loop sobre cada ação
for acao in lista_acoes:
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={acao}"
    
    # Fazendo a requisição HTTP
    page = requests.get(url, headers=headers)
    
    # Verificando se a requisição foi bem-sucedida
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Encontrando as tabelas que contêm os dados desejados
        tabelas = soup.select("table.w728")
        
        # Inicializando o dicionário para armazenar os dados da ação
        dados_dict = {'Ticker': acao}  # Inclui o ticker como chave

        for tabela in tabelas:  
            linhas = tabela.find_all('tr')  
            for linha in linhas:  
                colunas = linha.find_all('td')  
                if colunas:
                    for i in range(0, len(colunas), 2):
                        if i + 1 < len(colunas):
                            chave = colunas[i].get_text(strip=True).replace('?', '')
                            valor = colunas[i + 1].get_text(strip=True).replace('.', ',').replace('-', '0')
                            
                            # Verificando se a chave já existe no dicionário e modificando o nome da chave
                            if chave in dados_dict:
                                contador = 1
                                while f"{chave}_{contador}" in dados_dict:
                                    contador += 1
                                chave = f"{chave}_{contador}"

                            dados_dict[chave] = valor  

        # Adicionando os dados ao DataFrame
        df_temp = pd.DataFrame([dados_dict])  
        lista_dfs.append(df_temp)  

    else:
        print(f"Erro ao acessar {acao}: {page.status_code}")
    
    # Pausa para evitar bloqueios (recomendado entre 1 a 3 segundos)
    # time.sleep(1)

# Concatenando todos os DataFrames
df_final = pd.concat(lista_dfs, ignore_index=True)

# Exibindo o DataFrame organizado
print(df_final.columns)
