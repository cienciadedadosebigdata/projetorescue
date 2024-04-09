# Importando bibliotecas e configurações necessárias:
from prereqs import *
from functions import *
from conf_selenium import *
from conf_duckdb import *

import streamlit as st
import openai
import streamlit as st
import openai

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

# Título da aplicação
st.title('Análise de Dados com GPT-4')

# Verifica se o estado da sessão 'csv_content' existe, se não, inicializa como None
if 'csv_content' not in st.session_state:
    st.session_state['csv_content'] = None

# Cria botão para ler o conteudo do arquivo csv_final sem ser upload pois o arquivo já está salvo
if st.button('Ler arquivo CSV'):
    with open(csv_final, 'r') as file:
        # Salva o conteúdo do CSV no estado da sessão
        st.session_state['csv_content'] = file.read()

# Se o conteúdo do CSV foi carregado, prepara o prompt para o GPT-4
if st.session_state['csv_content'] is not None:
    prompt = f"Com base no arquivo CSV:\n\n{st.session_state['csv_content']}\n\n Me dê 10 insights interessantes sobre esses dados."

    # Exibição do prompt para conferência
    st.write('Prompt para análise de dados:')
    st.code(prompt)

    # Exibindo a resposta
    if st.button('Analisar com GPT-4'):
        with st.spinner('Analisando dados...'):
            try:
                # Configurando a chave da API da OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                client = OpenAI(api_key=api_key)
                # Criando uma conclusão de chat com GPT-4
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-4",  
                )
                st.write(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Erro ao analisar dados: {e}")