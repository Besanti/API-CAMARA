import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=' + str(idLegislatura)
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def obterGastosDeputado(idDeputado):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados/' + str(idDeputado) + '/despesas?ordem=DESC&ordenarPor=ano'
    r = requests.get(url)
    gastos = r.json()['dados']
    total_gastos = sum(gasto['valorLiquido'] for gasto in gastos)
    return total_gastos

st.title('Lista de Deputados em Exercício')

idLegislatura = st.slider('Escolha de qual legislatura você quer a lista de deputados', 50, 57, 57)

df = baixaDeputados(idLegislatura)

# Adiciona coluna de gastos
df['gastos'] = df['id'].apply(obterGastosDeputado)

st.header('Lista de deputados')
st.dataframe(df)
st.download_button('Baixar lista de deputados', data=df.to_csv(), file_name='deputados.csv', mime='text/csv')

st.header('Gráficos')
st.subheader('Número de deputados por partido')
st.bar_chart(df['siglaPartido'].value_counts())
st.subheader('Número de deputados por estado')
st.bar_chart(df['siglaUf'].value_counts())

st.header('Lista de deputados por estado')
coluna1, coluna2 = st.columns(2)
estado = coluna1.selectbox('Escolha um estado', sorted(df['siglaUf'].unique()), index=25)
partido = coluna2.selectbox('Escolha um partido', sorted(df['siglaPartido'].unique()))
df2 = df[(df['siglaUf'] == estado) & (df['siglaPartido'] == partido)]
st.markdown('---')

if df2.empty:
    st.subheader(':no_entry_sign: Sem deputados nesse estado filiados a esse partido! :crying_cat_face:')
else:
    for index, linha in df2.iterrows():
        with st.expander(linha['nome']):
            st.image(linha['urlFoto'], width=130)
            st.write('Nome: ' + linha['nome'])
            st.write('Partido: ' + linha['siglaPartido'])
            st.write('UF: ' + linha['siglaUf'])
            st.write('ID: ' + str(linha['id']))
            st.write('Email: ' + str(linha['email']))
            st.write('Gastos: R$ ' + str(linha['gastos']))

