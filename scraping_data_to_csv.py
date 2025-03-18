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
    numero_cotas = dados02[1]
    numero_cotas = dados02[1]
    
    #Dados de oscilação
    dados03 = soup.find_all('span', class_='oscil')
    osc_dia = dados03[0]
    osc_mes = dados03[1]
    osc_30dias = dados03[2]
    osc_12meses = dados03[3]
    osc_2025 = dados03[4]
    osc_2024 = dados03[5]
    osc_2023 = dados03[6]
    osc_2022 = dados03[7]
    osc_2021 = dados03[8]
    osc_2020 = dados03[9]

    #Dados indicadores
    dados04 = soup.find_all('td', class_='data w2')
    FFO_YIELD = dados04[0]
    PVP = dados04[3]
    FF0COTA = dados04[1]
    DIVIDENDOCOTA = dados04[2]
    VPCOTA = dados04[4]
    DIV_YIELD = dados01[18]
    

    #min_52_sem = soup.find('td', class_="data")[1]
    #max_52_sem = soup.find('td', class_="data")[2]
    

    dados_acoes['acoes'] = {
        "Papel": papel.text.strip() if papel else 'Não encontrado',
        "Cotação": cotacao.text.strip() if cotacao else 'Não encontrado',
        "Empresa": empresa.text.strip() if empresa else 'Não encontrado',
        "Min 52 sem": min_52_sem.text.strip() if min_52_sem else 'Não encontrado',
        "Max 52 sem": max_52_sem.text.strip() if max_52_sem else 'Não encontrado',
        'Valor de mercado': valor_mercado.text.strip() if valor_mercado else 'Não encontrado',
        'Nº de cotas': numero_cotas.text.strip() if numero_cotas else 'Não encontrado',
        'Oscilação do dia' : osc_dia.text.strip() if osc_dia else 'Não encontrado',
        'Oscilação de 30 dias' : osc_30dias.text.strip() if osc_30dias else 'Não encontrado',
        'Oscilação do mês' : osc_mes.text.strip() if osc_mes else 'Não encontrado',
        'Oscilação 12 meses' : osc_12meses.text.strip() if osc_12meses else 'Não encontrado',
        'Oscilação 2025' : osc_2025.text.strip() if osc_2025 else 'Não encontrado',
        'Oscilação 2024' : osc_2024.text.strip() if osc_2024 else 'Não encontrado',
        'Oscilação 2023' : osc_2023.text.strip() if osc_2023 else 'Não encontrado',
        'Oscilação 2022' : osc_2022.text.strip() if osc_2022 else 'Não encontrado',
        'Oscilação 2021' : osc_2021.text.strip() if osc_2021 else 'Não encontrado',
        'Oscilação 2020' : osc_2020.text.strip() if osc_2020 else 'Não encontrado',
        'FFO Yield' : FFO_YIELD.text.strip() if FFO_YIELD else 'Não encontrado',
        'Div. Yield' : DIV_YIELD.text.strip() if DIV_YIELD else 'Não encontrado',
        'PV/VP' : PVP.text.strip() if PVP else 'Não encontrado'
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


#print(dados01)
