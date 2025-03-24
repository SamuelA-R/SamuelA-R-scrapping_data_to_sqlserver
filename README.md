# Web Scraping de Dados Financeiros Fundamentalista
### Objetivo: Extrair e tratar os dados, Armazená-los no SQL Server, analisar os dados e disponibilizá-los de forma clara para acesso e visualização de insights utilizando Streamlit

📌 ***Tecnologias: Python (Requests, BeautifulSoup, Pandas, Json), SQL SERVER para armazenar os dados e Streamlit (relatório para visualização dos dados).***

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
- Iniciaremos extraindo os dados de todas as ações listadas na bolsa de valores. Para isso será necessária as seguintes bibliotecas:

```python
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
```
- Precisamos definir a URL da página que será acessada e os cabeçalhos para simular um navegador são definidos, no meu caso:
```python
url = "https://www.dadosdemercado.com.br/acoes"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
```
- O código abaixo vai fazer a requisição do html para obter as informações da página e verificar se a requisição foi bem-sucedida (status 200) antes de prosseguir. Para isso, o conteúdo HTML da página é processado com o BeautifulSoup para facilitar a extração dos dados:
 ```python
page = requests.get(url, headers=headers)
if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')
else:
    print(f"Erro ao acessar a página: {page.status_code}")
soup = BeautifulSoup(page.text, 'html.parser')
```
## 2️⃣ Integração dos dados no SQL Server

## 3️⃣ Relatório no Streamlit

### Disponibilizando o relatório no streamlit






📌 **Para eventuais dúvidas, conecte-se comigo no LinkedIn:**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/samuel-alves-ribeiro-017960246/)

📞 **Ou me chame pelo whatsapp Contato** : +55 44 99174-9358
