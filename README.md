# Web Scraping de Dados Financeiros Fundamentalista
### Objetivo: Extrair e tratar os dados, Armazená-los no SQL Server, analisar os dados e disponibilizá-los de forma clara para acesso e visualização de insights utilizando Streamlit

📌 ***Tecnologias: Python (Requests, BeautifulSoup, Pandas, JSON), SQL SERVER para armazenar os dados e Streamlit (relatório para visualização dos dados).***

🔹 ***Tarefas:**
- Criar um scraper para coletar dados.  
- Armazenar os dados extraídos em um banco do SQL Server.  
- Criar uma API ou script que consulte o banco.  
-	Analisar os dados utilizando Python e criar um relatório com Streamlit.

🔗 ***Estrutura da Integração Python + SQL + Streamlit***
✅ Python → Extração, tratamento avançado e automação
✅ SQL → Armazenamento, integração e otimização de consultas
✅ Streamlit → Visualização e análise interativa

📌 Fluxo do Processo:
1.	Python: Extrai, trata e carrega os dados no banco SQL.
2.	SQL: Armazena, processa e otimiza consultas.
3.	Streamlit: Conecta-se ao banco e visualiza os dados.

## 1️⃣ Scraping com Python
### Scraping das ações listadas na bolsa de valor
- Iniciaremos extraindo os dados de todas as ações listadas na bolsa de valores. Para isso será necessária as seguintes bibliotecas:

```python
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import pandas as pd
import time
import json
```
- requests: para fazer requisições `HTTP` ao site.

- BeautifulSoup: para fazer o parsing do `HTML` e extrair os dados.

- sleep (do time): para pausar o código por um tempo definido (ex: sleep(1) pausa por 1 segundo).

- datetime: para trabalhar com datas e horas (ex: pegar a data atual com datetime.now()).

- pandas: para transformar os dados em um DataFrame e facilitar a análise.

- time: para pausar entre requisições (evitando bloqueios) e medir tempo de execução.

- json: para trabalhar com dados no formato `JSON` (como salvar e carregar dicionários).
  
- Precisamos definir a `URL` da página que será acessada e os cabeçalhos para simular um navegador são definidos, no meu caso:
```python
url = "https://www.dadosdemercado.com.br/acoes"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
```
- O código abaixo vai fazer a requisição do `HTML` para obter as informações da página e verificar se a requisição foi bem-sucedida (`status 200`) antes de prosseguir. Para isso, o conteúdo HTML da página é processado com o BeautifulSoup para facilitar a extração dos dados:
 ```python
page = requests.get(url, headers=headers)
if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')
else:
    print(f"Erro ao acessar a página: {page.status_code}")
soup = BeautifulSoup(page.text, 'html.parser')
```
- Agora, criamos uma lista para armazenar o código de todas as ações listadas na bolsa, que será utilizada na extração no site Fundamentos. A função for vai percorrer toda a lista, utilizando o método `find_all`, que vai encontrar todas as tags `<strong>`


```python
dados = soup.find_all('strong')
lista = []
for data in dados:
    lista.append(data.text)
```

- Salvamos os dados extraidos em um arquivo de texto `acoes.txt`, onde cada ação é escrita em uma nova linha:
  
```python
with open("acoes.txt", "w") as f:
    for item in lista:
        f.write(item + '\n')  # Atualiza a lista de ações
```

### Scraping dos dados Fundamentus
- Extração dos dados fundamentalistas que vamos analisar
- Utilizaremos o metodo `with` para ler os tickers extraidos
- 
```python
with open("acoes.txt", "r") as fundamentus_file:
    lista_acoes = fundamentus_file.read().split()
```
- Define o cabeçalho da requisição simulando um navegador real para evitar que o site bloqueie a requisição e criamos uma lista para armazenar os dados de cada ação
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (...) Safari/537.36'
}

dados_json = []
```
- O bloco de código abaixo percorre cada ticker presente na `lista lista_acoes`, que foi lida previamente de um arquivo de texto. Para cada ticker, ele constrói a `URL` correspondente à página de detalhes dessa ação no site Fundamentus. Em seguida, faz uma requisição `HTTP` usando a biblioteca `requests`, passando um cabeçalho customizado para simular um navegador e evitar bloqueios do site. Se a requisição for bem-sucedida (`código de status 200`), o conteúdo `HTML` da página é processado com `BeautifulSoup`, que permite navegar e extrair as informações da estrutura da página.
O código então localiza todas as tabelas com a classe `w728`, que contêm os dados financeiros da ação. Ele percorre essas tabelas linha por linha e, dentro de cada linha, acessa as colunas com os nomes dos indicadores e seus respectivos valores. Os dados são extraídos 
em pares: o nome do indicador (`chave`) e o valor correpondente, já realizando um tratamento básico nos textos (como remoção de símbolos e padronização numérica). Antes de adicionar ao dicionário, o código verifica se a chave já existe — e, caso exista, renomeia a 
chave com um sufixo numérico para evitar sobrescrita. Ao final do processo para uma ação, todas as informações coletadas são armazenadas em um dicionário e adicionadas à lista `dados_json`, que armazenará os dados de todas as ações consultadas.
Esse processo se repete para cada ticker da lista, com uma pequena pausa (`sleep`) ao final de cada iteração para evitar que o site bloqueie as requisições por excesso de acessos em pouco tempo.
```python
for acao in lista_acoes:
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={acao}"
    
    # Faz a requisição HTTP para o site da Fundamentus
    page = requests.get(url, headers=headers)
    
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Seleciona todas as tabelas com a classe 'w728' (onde ficam os dados financeiros)
        tabelas = soup.select("table.w728")
        
        # Cria um dicionário para armazenar os dados da ação atual
        dados_dict = {'Ticker': acao}

        for tabela in tabelas:
            linhas = tabela.find_all('tr')  # Encontra todas as linhas da tabela
            for linha in linhas:
                colunas = linha.find_all('td')  # Encontra todas as colunas da linha
                if colunas:
                    # Percorre os pares de colunas (indicador e valor)
                    for i in range(0, len(colunas), 2):
                        if i + 1 < len(colunas):
                            # Extrai e limpa o nome do indicador
                            chave = colunas[i].get_text(strip=True).replace('?', '')  # remove espaços e interrogação

                            # Extrai e trata o valor:
                            valor = colunas[i + 1].get_text(strip=True) \
                                .replace('-', '0')      # substitui traços por zero
                                .replace('.', '')        # remove pontos (milhares)
                                .replace(',', '.')       # troca vírgula por ponto (notação decimal)
                                .replace('%', '')        # remove o símbolo de porcentagem
                            
                            # Evita duplicidade de chave no dicionário (ex: "ROE" aparecendo mais de uma vez)
                            if chave in dados_dict:
                                contador = 1
                                while f"{chave}_{contador}" in dados_dict:
                                    contador += 1
                                chave = f"{chave}_{contador}"

                            # Adiciona o par chave: valor ao dicionário da ação
                            dados_dict[chave] = valor

        # Adiciona o dicionário completo da ação à lista final
        dados_json.append(dados_dict)
```
## 2️⃣ Integração dos dados no SQL Server

## 3️⃣ Relatório no Streamlit

### Disponibilizando o relatório no streamlit






📌 **Para eventuais dúvidas, conecte-se comigo no LinkedIn:**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/samuel-alves-ribeiro-017960246/)

📞 **Ou me chame pelo whatsapp Contato** : +55 44 99174-9358
