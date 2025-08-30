import requests
from bs4 import BeautifulSoup
from time import sleep  # Importando a função sleep
from datetime import datetime

def atualizar_acoes():
    url = "https://www.dadosdemercado.com.br/acoes"

    # Definindo o cabeçalho User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Corrigindo a chamada da função, passando headers como um argumento nomeado
    page = requests.get(url, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        # Processamento do HTML aqui...
        # print(soup.prettify())  # Exibe o HTML de forma legível
    else:
        print(f"Erro ao acessar a página: {page.status_code}")
        return

    # Definindo o tipo da página, no caso html
    soup = BeautifulSoup(page.text, 'html.parser')

    # Inicializando o dicionário para armazenar os dados
    dados_acoes = {}

    dados = soup.find_all('strong')
    lista = []

    for data in dados:
        lista.append(data.text)

    # Salvando a lista como um arquivo .txt, sobrescrevendo o arquivo existente
    with open("acoes.txt", "w") as f:
        for item in lista:
            f.write(item + '\n')  # atualiza a lista de ações


