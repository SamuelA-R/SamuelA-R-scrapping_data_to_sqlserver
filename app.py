import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import plotly.express as px

##### Carregar e tratar os dados ######
df = pd.read_excel('dadosAcoes.xlsx')
df = df.drop(index=df.index[0:4]).reset_index(drop=True)
df = df[df['Papel'].notna() & (df['Papel'] != "")]

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


def graph(data_selection, valor1, valor2=None, valor3=None):
    data1 = data_selection[['Papel', valor1, 'Cotação']].dropna().sort_values(valor1, ascending=False).head(20)
    fig1 = go.Figure(go.Bar(x=data1[valor1], y=data1["Papel"], orientation='h', marker=dict(color='teal')))
    fig1.update_traces(
        hovertemplate='<b>Papel:</b> %{y}<br><b>' + valor1 + ':</b> 📈 %{x}<br><b>Cotação:</b> 💰 %{customdata[0]}',
        customdata=data1[['Cotação']]
    )
    fig1.update_layout(hoverlabel=dict(bgcolor="yellow", font_color="black"))
    fig1.update_layout(yaxis=dict(categoryorder="total ascending"), title=f"Gráfico de {valor1}", height=600)

    if valor2 and valor2 in data_selection.columns:
        data2 = data_selection[['Papel', valor2, 'Cotação']].dropna().sort_values(valor2, ascending=False).head(20)
        fig2 = go.Figure(go.Bar(x=data2[valor2], y=data2["Papel"], orientation='h', marker=dict(color='teal')))
        fig2.update_traces(
            hovertemplate='<b>Papel:</b> %{y}<br><b>' + valor2 + ':</b> 📈 %{x}<br><b>Cotação:</b> 💰 %{customdata[0]}',
            customdata=data2[['Cotação']]
        )
        fig2.update_layout(hoverlabel=dict(bgcolor="yellow", font_color="black"))
        fig2.update_layout(yaxis=dict(categoryorder="total ascending"), title=f"Gráfico de {valor2}", height=600)

    if valor3 and valor3 in data_selection.columns:
        data3 = data_selection[['Papel', valor3, 'Cotação']].dropna().sort_values(valor3, ascending=False).head(20)
        fig3 = go.Figure(go.Bar(x=data3[valor3], y=data3["Papel"], orientation='h', marker=dict(color='teal')))
        fig3.update_traces(
            hovertemplate='<b>Papel:</b> %{y}<br><b>' + valor3 + ':</b> 📈 %{x}<br><b>Cotação:</b> 💰 %{customdata[0]}',
            customdata=data3[['Cotação']]
        )
        fig3.update_layout(hoverlabel=dict(bgcolor="yellow", font_color="black"))
        fig3.update_layout(yaxis=dict(categoryorder="total ascending"), title=f"Gráfico de {valor3}", height=600)

    # Plotagem dinâmica
    if valor2 and valor3:
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig1, use_container_width=True)
        col2.plotly_chart(fig2, use_container_width=True)
        col3.plotly_chart(fig3, use_container_width=True)
    elif valor2:
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig1, use_container_width=True)
        col2.plotly_chart(fig2, use_container_width=True)
    else:
        st.plotly_chart(fig1, use_container_width=True)


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
    st.sidebar.image("bull.png", caption="Online Analytics from Fundamentus")
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
    graph(data_selection, "Últimos 12 meses", "Receita Líquida_1", "Lucro Líquido_1")

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


#Pagina 2
elif selected == "Contato":
    st.title("Contato")
    st.markdown("""
    **Autor**: Samuel  
    **Email**: samuelalvesribeiro111@gmail.com  
    **LinkedIn**: [linkedin.com/in/samuel-alves-ribeiro](https://www.linkedin.com/in/samuel-alves-ribeiro-017960246/)
    """)
