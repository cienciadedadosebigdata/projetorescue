## Todas as funções do projeto Rescue

## Importa bibliotecas
from prereqs import *
from conf_selenium import *
from conf_duckdb import *

# Função para aguardar o download completo do arquivo
def wait_for_download(download_dir):
    # Espera até que o arquivo .crdownload não esteja mais no diretório
    while any(".crdownload" in filename for filename in os.listdir(download_dir)):
        time.sleep(1)

## Processa os anos baixando o conteudo com Selenium
def processa_anos(ano_inicio, ano_fim):
    for ano in range(ano_inicio, ano_fim+1):
        # Verifica se o diretorio xls_dir existe, se não cria:
        if not os.path.exists(xls_dir):
            os.makedirs(xls_dir)
        # Verifica se o arquivo já existe para o ano atual
        if os.path.exists(os.path.join(download_dir, f'dados_salic_pj_{ano}.xls')):
            print(f"Arquivo para o ano {ano} já existe, pulando para o próximo ano.")
            continue
        try:
            # Abre a URL inicial
            driver.get("http://sistemas.cultura.gov.br/salicnet/Salicnet/Salicnet.php")

            # Espera e clica no link 'Incentivadores'
            incentivadores_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Incentivadores')))
            incentivadores_link.click()

            # Espera e clica no link 'Por Ano, Região e UF'
            por_ano_regiao_uf_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Por Ano, Região e UF')))
            por_ano_regiao_uf_link.click()

            # Mudar o contexto para o iframe
            iframe = wait.until(EC.presence_of_element_located((By.ID, 'iframe_Salicnet')))
            driver.switch_to.frame(iframe)

            # Espera pelo elemento dropdown 'ano' e verifica se a opção desejada está presente
            select_element = wait.until(EC.presence_of_element_located((By.NAME, 'ano')))
            select = Select(select_element)

            # Seleciona o ano, removendo espaços em branco extras, se houver
            select.select_by_value(str(ano))

            # Encontra o elemento dropdown para seleção do tipo de pessoa
            tipo_pessoa_dropdown = wait.until(EC.presence_of_element_located((By.NAME, 'tipopessoa')))
            tipo_pessoa_select = Select(tipo_pessoa_dropdown)

            # Seleciona "Pessoa Jurídica" pelo seu texto visível ou valor
            tipo_pessoa_select.select_by_visible_text('Pessoa Jurídica')  # ou use select_by_value se você souber o valor

            # Espera e clica no botão 'OK' para iniciar o download
            ok_button = wait.until(EC.element_to_be_clickable((By.NAME, 'sub_form')))
            ok_button.click()

            # Espera e clica no botão 'XLS' para iniciar o download
            xls_button = wait.until(EC.element_to_be_clickable((By.NAME, 'sc_b_xls')))
            xls_button.click()

            # Agora clica no link fazendo o download do XLS
            xls_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/tmp/sc_xls_')]")))
            xls_link.click()

            # Aguarda um tempo adicional para o download começar
            time.sleep(5)

            # Aguarda o download ser concluído
            wait_for_download(download_dir)

            # Encontra o último arquivo baixado (o mais recente)
            list_of_files = glob.glob(f'{download_dir}/*.xls')  # Pode ajustar a extensão se necessário

            # Verifica se pelo menos um arquivo foi baixado
            while not list_of_files:
                time.sleep(1)
                list_of_files = glob.glob(f'{download_dir}/*.xls')

            latest_file = max(list_of_files, key=os.path.getctime)

            # Define o novo nome do arquivo
            new_file_name = os.path.join(download_dir, f'dados_salic_pj_{ano}.xls')

            # Renomeia o arquivo
            os.rename(latest_file, new_file_name)

            # Se precisar interagir com a página principal novamente
            driver.switch_to.default_content()

            # Aguarda um tempo para garantir que a ação tenha sido realizada
            time.sleep(5)

        except Exception as e:
            print(f"Ocorreu um erro no ano {ano}: {e}")
            continue  # Continua para o próximo ano no caso de erro

    # Fecha o navegador
    driver.quit()

## Converte os arquivos XLS para CSV
def converte_xls_para_csv(xls_dir, csv_dir):
    # Lista todos os arquivos .xls no diretório
    xls_files = [f for f in os.listdir(xls_dir) if f.endswith('.xls')]

    # Loop para converter e mover os arquivos
    for xls_file in xls_files:
        # Obtém o caminho completo para o arquivo .xls
        xls_path = os.path.join(xls_dir, xls_file)

        # Lê o arquivo .xls usando o pandas
        df = pd.read_excel(xls_path)

        # Remove a extensão .xls do nome do arquivo e adiciona .csv
        csv_file = os.path.splitext(xls_file)[0] + '.csv'

        # Obtém o caminho completo para o arquivo .csv (no diretório csv_dir)
        # cria o diretorio se ele não existir
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        csv_path = os.path.join(csv_dir, csv_file)

        # Adiciona a coluna 'ano' com o ano do arquivo
        ano = int(xls_file.split('_')[-1].split('.')[0])
        df['ano'] = ano

        # Salva o DataFrame como um arquivo .csv
        df.to_csv(csv_path, index=False, encoding='utf-8')

        # Exclui o arquivo .xls após a conversão
        os.remove(xls_path)

    print("Conversão concluída e arquivos .xls excluídos no diretório xls.")

## Cria uma função que junta todos os arquivos CSV em um único arquivo
def unico_csv(csv_dir, csv_final):
    # Desativa o Warning do downcasting
    pd.set_option('future.no_silent_downcasting', True)
    # Lista todos os arquivos .csv no diretório
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

    # Loop para ler e concatenar os arquivos .csv
    dfs = []
    for csv_file in csv_files:
        # Obtém o caminho completo para o arquivo .csv
        csv_path = os.path.join(csv_dir, csv_file)

        # Lê o arquivo .csv usando o pandas
        df = pd.read_csv(csv_path)

        # Altera todos os valores 'conIncentivadorMecenatoPorRegiaoUF' na coluna 'ano' para 1993
        #df['ANO'] = df['ANO'].replace('conIncentivadorMecenatoPorRegiaoUF', 1993)

        # Adiciona o DataFrame à lista
        dfs.append(df)

    # Concatena todos os DataFrames na lista
    result = pd.concat(dfs, ignore_index=True)

    # Salva o DataFrame concatenado em um único arquivo .csv
    result.to_csv(csv_final, index=False, encoding='utf-8')

    # Remove pastas xls e csv
    shutil.rmtree(xls_dir)
    shutil.rmtree(csv_dir)

    print(f"Arquivo {csv_final} criado com sucesso.")


## Função que cria tabela no DuckDB
def cria_tabela_duckdb(csv_final, db_path):
    # Verifica se o arquivo CSV existe
    if not os.path.exists(csv_final):
        print(f"Arquivo {csv_final} não encontrado.")
        return

    # Conecta ao banco de dados DuckDB
    con = duckdb.connect(db_path)

    # Exclui a tabela existente, se houver
    con.execute("DROP TABLE IF EXISTS salic_data")

    # Cria uma nova tabela no DuckDB a partir do arquivo .csv
    con.execute(f"CREATE TABLE salic_data AS SELECT * FROM read_csv_auto('{csv_final}')")

    print("Tabela criada no DuckDB com sucesso.")

## Função que faz consultas no DuckDB
def consulta_duckdb(consulta, db_path):
    # Verifica se o banco de dados DuckDB existe
    if not os.path.exists(db_path):
        print(f"Banco de dados {db_path} não encontrado.")
        return

    # Conecta ao banco de dados DuckDB
    con = duckdb.connect(db_path)

    # Executa a consulta e retorna o resultado como um DataFrame do pandas
    result = con.execute(consulta).fetch_df()

    return result
