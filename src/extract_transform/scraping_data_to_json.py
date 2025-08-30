import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

def coletar_dados_acoes(input_file="acoes.txt", output_file="dados_json2.json"):
    with open(input_file, "r") as fundamentus_file:
        lista_acoes = fundamentus_file.read().split()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    dados_json = []

    # Loop sobre cada ação para extrair os dados
    for acao in lista_acoes:
        url = f"https://www.fundamentus.com.br/detalhes.php?papel={acao}"
        
        # requisição
        page = requests.get(url, headers=headers)
        
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            
            tabelas = soup.select("table.w728")
            
            dados_dict = {'Ticker': acao}  # Inclui o ticker como chave

            for tabela in tabelas:  
                linhas = tabela.find_all('tr')  
                for linha in linhas:  
                    colunas = linha.find_all('td')  
                    if colunas:
                        for i in range(0, len(colunas), 2):
                            if i + 1 < len(colunas):
                                chave = colunas[i].get_text(strip=True).replace('?', '')
                                valor = colunas[i + 1].get_text(strip=True).replace('.', '').replace(',', '.').replace('%', '')
                                
                                # Verificando se a chave já existe no dicionário e modificando o nome da chave
                                if chave in dados_dict:
                                    contador = 1
                                    while f"{chave}_{contador}" in dados_dict:
                                        contador += 1
                                    chave = f"{chave}_{contador}"

                                dados_dict[chave] = valor  

            dados_json.append(dados_dict)
        
        else:
            print(f"Erro ao acessar {acao}: {page.status_code}")
        
        # Pausa para evitar bloqueios
        time.sleep(0.2)

    # Convertendo os dados para JSON
    json_data = json.dumps(dados_json, ensure_ascii=False)

    # Carregar JSON para DataFrame
    df = pd.read_json(json_data, orient="records")

    # Remover as primeiras 4 linhas e resetar o índice
    df = df.drop(index=df.index[0:4]).reset_index(drop=True)
    df = df.drop(columns=['Oscilações', '', 'Últimos 12 meses', ])  # Remove colunas inúteis
    df = df[df['Papel'].notna() & (df['Papel'] != "")]  # Retira papéis não encontrados

    # Salvar em arquivo JSON final
    df.to_json(output_file)
    print(f"Arquivo salvo: {output_file}")

    return df
