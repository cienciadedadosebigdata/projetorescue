# Importando bibliotecas e configurações necessárias:
from prereqs import *
from functions import *
from conf_selenium import *
from conf_duckdb import *

import streamlit as st

# Título principal
st.title('Projeto Rescue - Dados SALIC')

# Criar uma linha para separar o título
st.markdown('---')

# Dividindo a página em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader('Processamento de Anos')
    ano_inicio = st.number_input('Insira o ano de início', min_value=1993, max_value=2024, value=1993)
    ano_fim = st.number_input('Insira o ano final', min_value=1993, max_value=2024, value=1995)
    processar = st.button('Processar anos')

with col2:
    st.subheader('Manipulação de Arquivos CSV')
    converter = st.button('Converter XLS para CSV')
    gerar_csv_unico = st.button('Gerar CSV único')
    criar_tabela = st.button('Criar tabela no DuckDB')

# Executando as ações fora do contexto das colunas para melhor organização
if processar:
    processa_anos(ano_inicio, ano_fim)
    st.success('Anos processados com sucesso.')

if converter:
    converte_xls_para_csv(xls_dir, csv_dir)
    st.success('Arquivos XLS convertidos para CSV com sucesso.')

if gerar_csv_unico:
    unico_csv(csv_dir, csv_final)
    st.success('CSV único gerado com sucesso.')

if criar_tabela:
    cria_tabela_duckdb(csv_final, db_path)
    st.success('Tabela criada no DuckDB com sucesso.')

# Área para consulta SQL
st.subheader('Consulta SQL')
consulta = st.text_area('Insira sua consulta SQL aqui:', height=150)
executar = st.button('Executar consulta')

# Execução da consulta SQL
if executar:
    resultado = consulta_duckdb(consulta, db_path)
    if resultado is not None:
        # Formatando colunas numéricas e exibindo resultados
        for col in resultado.columns:
            if resultado[col].dtype == 'float64':
                resultado[col] = resultado[col].apply(lambda x: "{:.0f}".format(x))
        st.dataframe(resultado)
    else:
        st.error('Erro ao executar a consulta.')

# Nota: Pode-se adicionar funcionalidades visuais como progress bars, spinners e placeholders para melhorar a experiência do usuário.
