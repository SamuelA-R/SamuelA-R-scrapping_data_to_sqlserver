import requests
from bs4 import BeautifulSoup
from time import sleep  # Importando a função sleep

url = "https://www.fundamentus.com.br/detalhes.php?papel=AAZQ11"

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

# Definindo o tipo da página, no caso html
soup = BeautifulSoup(page.text, 'html.parser')

# Inicializando o dicionário para armazenar os dados
dados_acoes = {}

try:
    # Extrair os principais indicadores da página
    papel = soup.find('td', class_="data w35")
    cotacao = soup.find('td', class_="data destaque w3")
    empresa = soup.find('td', class_="data")

    dados01 = soup.find_all('td', class_="data")
    Data_ult_cot = dados01[3]
    min_52_sem = dados01[5]  # Segundo elemento
    max_52_sem = dados01[7]  # Terceiro elemento

    dados02 = soup.find_all('td', class_="data w3")
    valor_mercado = dados02[0]
    numero_cotas = dados02[1]

    #min_52_sem = soup.find('td', class_="data")[1]
    #max_52_sem = soup.find('td', class_="data")[2]
    

    dados_acoes['acoes'] = {
        "Papel": papel.text.strip() if papel else 'Não encontrado',
        "Cotação": cotacao.text.strip() if cotacao else 'Não encontrado',
        "Empresa": empresa.text.strip() if empresa else 'Não encontrado',
        "Min 52 sem": min_52_sem.text.strip() if min_52_sem else 'Não encontrado',
        "Max 52 sem": max_52_sem.text.strip() if max_52_sem else 'Não encontrado',
        'Valor de mercado': valor_mercado.text.strip() if valor_mercado else 'Não encontrado',
        'Nº de cotas': numero_cotas.text.strip() if numero_cotas else 'Não encontrado'
        }

    print("✅ Dados extraídos com sucesso")

except Exception as e:
    print(f'Erro ao extrair dados de: {e}')

# Aguardar 1 segundo entre as requisições
sleep(1)

print(dados_acoes)

'''# Abrindo o arquivo CSV para escrita no modo append
with open(csv_file, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=dados_acoes.keys())

    # Escreve o cabeçalho apenas se o arquivo ainda não existir
    if not file_exists:
        writer.writeheader()

    # Escreve os dados da nova ação
    writer.writerow(dados_acoes)

print("✅ Dados adicionados em 'dados_acoes.csv'")'''
