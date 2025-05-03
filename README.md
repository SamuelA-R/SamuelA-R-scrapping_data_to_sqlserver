# Web Scraping de Dados Financeiros Fundamentalista
### Objetivo: Extrair e tratar os dados, Armazená-los no SQL Server, analisar os dados e disponibilizá-los de forma clara para acesso e visualização de insights utilizando Streamlit

***Tecnologias: Python (Requests, BeautifulSoup, Pandas, JSON), SQL SERVER para armazenar os dados e Streamlit (relatório para visualização dos dados).***

***Tarefas:**
- Criar um scraper para coletar dados.  
- Armazenar os dados extraídos em um banco do SQL Server.  
- Criar uma API ou script que consulte o banco.  
-	Analisar os dados utilizando Python e criar um relatório com Streamlit.

***Estrutura da Integração Python + SQL + Streamlit***
- ✅ Python → Extração, tratamento avançado e automação
- ✅ SQL → Armazenamento, integração e otimização de consultas
- ✅ Streamlit → Visualização e análise interativa

Fluxo do Processo:
1.	Python: Extrai, trata e carrega os dados no banco SQL.
2.	SQL: Cria, processa e otimiza consultas.
3.	Streamlit: Conecta-se ao banco e visualiza os dados.

## 1️⃣ Extraction and transform: Scraping com Python
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
                            valor = colunas[i + 1].get_text(strip=True).replace('.', '').replace(',','.').replace('%', '')
                            
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
```
- Agora, convetemos os dados para dataframe para que possamos tratalos e carregamos com pandas.
```python
json_data = json.dumps(dados_json, ensure_ascii=False)
df = pd.read_json(json_data, orient="records")
```
- Agora excluiremos as quatro primeiras linhas do dataframe que possui dados inuteis adicionadas na extração e excluiremos as colunas `Osciações` e `últimos 12 meses` e, por fim, vamos retirar os dados de ações não encontradas de nosso dataframe e salvar novamente no formato `JSON` para inserir os dados em nosso BD.
```python
# Remover as primeiras 4 linhas e resetar o índice
df = df.drop(index=df.index[0:4]).reset_index(drop=True)
df = df.drop(columns=['Oscilações', '', 'Últimos 12 meses', ]) # Remove as colunas inuteis criadas na hora do scraping
df = df[df['Papel'].notna() & (df['Papel'] != "")] # Retira as colunas de papeis não encontrados


df.to_json('dados_json2.json')
```
## 2️⃣ Load: Integração dos dados no SQL Server
- Nestá etapa, primeiro precisamos criar o nosso banco de dados no SQL Server. Para isso deixei o código SQL para criação do database e da tabela na pasta `SQL Server`.
- Já criado o banco, iremos inserir os dados utilizando as seguintes bibliotecas:
```python
import pyodbc
import pandas as pd
```
    - pyodbc: para conectar-se ao banco de dados e inserir os dados na tabela:
    - pandas: para converter o arquivo salvo `JSON` em dataframe para que possamos interar sobre os dados e inserir em nosso `SGDB`.

- Primeiro criaremos a nossa função `conecta_ao_banco` de dados
```python
def conecta_ao_banco(driver='SQL Server', server='SAMUEL\\MSSQLSERVER01', database='Dados_scraping', trusted_connection="yes"):
    string_conexao = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};"
    conexao = pyodbc.connect(string_conexao)
    cursor = conexao.cursor()
    return conexao, cursor
```
- Ela recebe como parâmetros o `driver`, o `servidor`, o `nome do banco de dados` e se a conexão é autenticada pelo Windows (`via Trusted_Connection`).
- A string de conexão (`string_conexao`) é montada com esses parâmetros e, em seguida, o pyodbc.connect é usado para abrir a conexão.

- Por fim, a função retorna dois objetos:
    - conexao: o objeto de conexão com o banco;
    - cursor: o objeto que permite executar comandos `SQL` dentro dessa conexão.

- Agora, vamos inserior os dados em nosso banco.
- Primeiro criaremos nossa função `try` que vai "tentar" realizar a conexão com nosso banco.
```python
try:
    conexao, cursor = conecta_ao_banco()
    print("Conexão estabelecida!")
```
- Agora vamos armazenar o nome das colunas do nosso dataframe (que são as mesmas que criamos no SQL Server em SQL).
``` python
nomes_colunas = ", ".join(f"[{col}]" for col in dados.columns)
```
- Agora geramos os placeholders para cada valor de coluna (placeholders são espaços reservados (?) usados na query SQL para inserir os valores de forma segura e automática).
```python
placeholders = ", ".join("?" for _ in dados.columns)
```
- Agora inserimos os dados do Dataframe nas colunas existentes da tabela utilizando a função `FOR`:
```python
for _, row in dados.iterrows():
  # aqui estamos pegando os valores da linha e substituindo qualquer NaN por None
  valores = tuple(row[col] if pd.notna(row[col]) else None for col in dados.columns)
        
  # monta a query de inserção
  query = f"INSERT INTO ACOES ({nomes_colunas}) VALUES ({placeholders})"
        
  # executa a query passando os valores da linha
  cursor.execute(query, valores)
  # confirma as alterações no banco
  conexao.commit()
  print("Dados inseridos com sucesso!")
```
- Por fim, caso de erro, utilizamos o except, printando o erro para que possamos corrigir caso ocorra:
```python
except Exception as e:
    print("Erro:", e)
```

## 3️⃣ Dashboard: Relatório no Streamlit
- Será necessária as seguintes bibliotecas:

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import plotly.express as px
import pyodbc
```
    Utilidades de cada biblioteca:
    - Streamlit: construir a interface web
    - Pandas: manipular os dados para análise
    - Plotly (go e express): criar gráficos para a análise
    - Streamlit_option_menu: criar menu de botões com multiplas páginas
    - pyodbc: conectar-se ao banco de dados SQL Server e carregar os dados

- Iniciamos conctando ao banco de dados e realizando a query de todos os dados de nossa tabela ACOES criada. Após isso armazenamos os dados como dataframe na variável df

```python
def conecta_ao_banco(driver='SQL Server', server='SAMUEL\\MSSQLSERVER01', database='Dados_scraping', trusted_connection="yes"):
    string_conexao = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};"
    conexao = pyodbc.connect(string_conexao)
    cursor = conexao.cursor()
    return conexao, cursor

conexao, cursor = conecta_ao_banco()
print("Conexão estabelecida!")
# Consultar a tabela 'ACOES' diretamente e criar o DataFrame
query = "SELECT * FROM ACOES"
df = pd.read_sql(query, conexao)
```

Ao fazermos o carregamento dos dados, primeiro convertemos as colunas númericas para o tipo float
```python
def converter_tipo(table):
    for i in df.columns:
        try:
            table[i] = table[i].astype(float)
        except ValueError:
            pass
    return table

dados = converter_tipo(df)
```
Após isso vamos criar algumas funções para construir nosso dashboard:
- Função para os filtros multiselect laterais:
```python
def slidebar_filtro(dados_coluna, nome_slider):
    opcoes = list(dados_coluna.unique())
    selecao = st.sidebar.multiselect(label=f"{nome_slider}", options=opcoes)
    return selecao if selecao else opcoes
```

- Função que vai exibir a tabela em nosso dashboard

```python
def Home(data_selection):
    with st.expander('Tabular'):
        all_columns = data_selection.columns.tolist()
        selected_columns = st.multiselect(
            'Filter:',
            options=['Selecionar Tudo'] + all_columns,
            default=[]
        )
        showData = all_columns if 'Selecionar Tudo' in selected_columns else selected_columns
        st.write(data_selection[showData])
```
- Criaremos agora a função que vai gerar nosso gráfico de barras, nosso gráfico será na horizontal e hovertemplate será o nosso tooltip
```python
def gerar_grafico(data, valor):
    data_filtrada = data[['Papel', valor, 'Cotação']].dropna().sort_values(valor, ascending=False).head(20)
    fig = go.Figure(go.Bar(
        x=data_filtrada[valor],
        y=data_filtrada["Papel"],
        orientation='h',
        marker=dict(color='teal'),
        customdata=data_filtrada[['Cotação']],
        hovertemplate='<b>Papel:</b> %{y}<br><b>' + valor + ':</b> 📈 %{x}<br><b>Cotação:</b> 💰 %{customdata[0]}'
    ))
    fig.update_layout(
        hoverlabel=dict(bgcolor="yellow", font_color="black"),
        yaxis=dict(categoryorder="total ascending"),
        title=f"Gráfico de {valor}",
        height=600
    )
    return fig
```


- Agora criaremos a função que vai exibir os 3 gráficos lado a lado em nosso dashboard
```
def graph(df_filtrado, col1, col2=None, col3=None):
    colunas = [col1]
    if col2: colunas.append(col2)
    if col3: colunas.append(col3)

    cols = st.columns(len(colunas))
    for i, col in enumerate(colunas):
        with cols[i]:
            fig = gerar_grafico(df_filtrado, col)
            st.plotly_chart(fig, use_container_width=True)
```

- Gráfico de linhas da página 2
  
```python
#grafico de linhas
def line_graph(data_selection, valor):
    data = data_selection[['Papel', 'Ano', valor]].dropna()

    fig = px.line(
        data,
        x='Ano',
        y=valor,
        color='Papel',
        markers=True,
        title=f"Evolução de {valor} por Papel",
    )

    fig.update_traces(
        hovertemplate='<b>Papel:</b> %{fullData.name}<br><b>' + valor + ':</b> %{y}<br><b>Ano:</b> %{x}'
    )

    fig.update_layout(
        hoverlabel=dict(bgcolor="yellow"),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
```

- Agora criaremos o `option_menu` para criar as páginas para navegação no topo do sidebar, com ícones e estilos personalizados

```python
########## MENU LATERAL #############
with st.sidebar:
    st.sidebar.image("bull-market.png", caption="Online Analytics from Fundamentus")
    #Imagem inicial
    selected = option_menu(
        menu_title=None,
        options=["Home", "Histórico", "Contato"],
        icons=["house", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#f8f9fa"},
            "nav": {"justify-content": "center"},
            "icon": {"color": "black", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
                "color": "black",  # Cor do texto normal
            },
            "nav-link-selected": {
                "background-color": "#ff002f",
                "color": "black",  # Cor do texto quando selecionado
            },
        }
    )
```
- Criação da página "Home"
```python
if selected == "Home":
    ########## SIDEBAR ##################
    st.markdown("""
    <h1 style='text-align: center; background-color: #ff002f; color: white; padding: 10px; border-radius: 8px;'>
        Dashboard - Indicadores
    </h1>
    """, unsafe_allow_html=True)

    st.sidebar.header("Filtros")

    # Filtros primeiro!
    acoes_filtro = slidebar_filtro(dados['Papel'], "Ações")
    tipo_empresa = slidebar_filtro(dados['Tipo'], "Tipo")
    empresa = slidebar_filtro(dados['Empresa'], "Empresa")
    setor = slidebar_filtro(dados['Setor'], "Setor")
    subsetor = slidebar_filtro(dados['Subsetor'], "Subsetor")

    # Depois dos filtros, aplicamos a filtragem
    data_selection = dados.query(
        "(Papel in @acoes_filtro or @acoes_filtro == []) & "
        "(Tipo in @tipo_empresa or @tipo_empresa == []) & "
        "(Empresa in @empresa or @empresa == []) & "
        "(Setor in @setor or @setor == []) & "
        "(Subsetor in @subsetor or @subsetor == [])"
    )

    Home(data_selection)

    st.markdown("<h3 style='text-align: center;'>Rentabilidade e Retorno</h3>", unsafe_allow_html=True)
    graph(data_selection, "P/L", "LPA", "Div. Yield")

    st.markdown("<h3 style='text-align: center;'>Margens e Avaliação</h3>", unsafe_allow_html=True)
    graph(data_selection, "Marg. EBIT", "EV / EBIT")
    graph(data_selection, "ROE", "ROIC", "EBIT / Ativo")

    st.markdown("<h3 style='text-align: center;'>Eficiência Operacional</h3>", unsafe_allow_html=True)
    graph(data_selection, "Marg. Bruta", "Marg. Líquida", "Giro Ativos")

    st.markdown("<h3 style='text-align: center;'>Endividamento e Liquidez</h3>", unsafe_allow_html=True)
    graph(data_selection, "Dív. Líquida", "Dív. Bruta", "Liquidez Corr")

    st.markdown("<h3 style='text-align: center;'>Tamanho e Valor da Empresa</h3>", unsafe_allow_html=True)
    graph(data_selection, "Valor de mercado", "Valor da firma", "P/VP")

    st.markdown("<h3 style='text-align: center;'>Avaliação por Ativos</h3>", unsafe_allow_html=True)
    graph(data_selection, "P/Ativos", "P/Cap. Giro", "P/Ativ Circ Liq")

    st.markdown("<h3 style='text-align: center;'>Desempenho Operacional</h3>", unsafe_allow_html=True)
    graph(data_selection, "Receita Líquida", "Lucro Líquido", "EBIT")

    st.markdown("<h3 style='text-align: center;'>Evolução dos Últimos Anos</h3>", unsafe_allow_html=True)
    graph(data_selection, "Receita Líquida_1", "Lucro Líquido_1")
```
- Na página "Histórico", criamos os mesmos filtros da página anterior para permitir a seleção dos dados. Em seguida, utilizamos a função `melt` para criar a variável linha, que transforma as colunas de anos (como 2020, 2021, etc.) em linhas. Isso reorganiza os dados no formato ideal para construir o gráfico de linhas com a evolução das cotações ao longo do tempo.

```python
elif selected == "Histórico":
...
    linha = pd.melt(data_selection, id_vars=['Papel'], value_vars=['2020', '2021', '2022', '2023', '2024', '2025'],
                    var_name='Ano', value_name='Valor')
    

    line_graph(linha, 'Valor')
```


📌 **Para eventuais dúvidas, conecte-se comigo no LinkedIn:**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/samuel-alves-ribeiro-017960246/)

📞 **Ou me chame pelo whatsapp Contato** : +55 44 99174-9358
