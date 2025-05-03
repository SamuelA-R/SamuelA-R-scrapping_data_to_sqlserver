import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import plotly.express as px
import pyodbc

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

def converter_tipo(table):
    for i in df.columns:
        try:
            table[i] = table[i].astype(float)
        except ValueError:
            pass
    return table

dados = converter_tipo(df)

######### FUNÇÕES ####################
def slidebar_filtro(dados_coluna, nome_slider):
    opcoes = list(dados_coluna.unique())
    selecao = st.sidebar.multiselect(label=f"{nome_slider}", options=opcoes)
    return selecao if selecao else opcoes

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

def graph(df_filtrado, col1, col2=None, col3=None):
    colunas = [col1]
    if col2: colunas.append(col2)
    if col3: colunas.append(col3)

    cols = st.columns(len(colunas))
    for i, col in enumerate(colunas):
        with cols[i]:
            fig = gerar_grafico(df_filtrado, col)
            st.plotly_chart(fig, use_container_width=True)


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


############ Páginas #####################

#Pagina 1
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

#Pagina 2
elif selected == "Histórico":
    ########## SIDEBAR ##################
    st.markdown("""
    <h1 style='text-align: center; background-color: #ff002f; color: white; padding: 10px; border-radius: 8px;'>
        Dashboard - Histórico de cotação
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

    #tratamento dos dados históricos

    linha = pd.melt(data_selection, id_vars=['Papel'], value_vars=['2020', '2021', '2022', '2023', '2024', '2025'],
                    var_name='Ano', value_name='Valor')
    

    line_graph(linha, 'Valor')


#Pagina 3
elif selected == "Contato":
    st.title("📬 Formas de Contato")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(
            """
            <div style="text-align: center;">
                <p style="font-weight: bold; font-size: 18px;">GitHub</p>
                <a href="https://github.com/SamuelA-R/SamuelA-R-scrapping_data_to_sqlserver" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/9919?s=200&v=4" width="100" style="border-radius: 50%;">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:
        st.markdown("""
        ### Samuel Alves Ribeiro  
        Analista de Dados | Economista  

        📧 **Email**: samuelalvesribeiro111@gmail.com  
        """)

        # Botão azul do LinkedIn
        st.markdown(
            """
            <a href="https://www.linkedin.com/in/samuel-alves-ribeiro-017960246/" target="_blank">
                <button style="background-color:#0A66C2; color:white; padding:10px 20px; border:none; border-radius:5px; font-size:16px; cursor:pointer;">
                    Conectar no LinkedIn
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

        # Botão do GitHub
        st.markdown(
            """
            <a href="https://medium.com/@samuelalvesribeiro111" target="_blank">
                <button style="background-color:#24292e; color:white; padding:10px 20px; border:none; border-radius:5px; font-size:16px; margin-top:10px; cursor:pointer;">
                    🔗 Ver meu Medium
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown(
        """
        Se tiver alguma dúvida ou quiser discutir um projeto, sinta-se à vontade para me enviar um e-mail ou me conectar no LinkedIn.  

        O código completo deste projeto está disponível no meu GitHub. Clicando no botão acima você encontrará todo o código com explicações detalhadas no README.
        """
    )
