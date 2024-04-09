## Todas as funções do projeto Rescue

## Importa bibliotecas
from prereqs import *
from conf_selenium import *

# Função para aguardar o download completo do arquivo
def wait_for_download(download_dir):
    # Espera até que o arquivo .crdownload não esteja mais no diretório
    while any(".crdownload" in filename for filename in os.listdir(download_dir)):
        time.sleep(1)

## Processa os anos baixando o conteudo com Selenium
def processa_anos(ano_inicio, ano_fim):
    for ano in range(ano_inicio, ano_fim+1):
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

            ## Agora clica no link fazendo o download do XLS
            xls_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/tmp/sc_xls_')]")))
            xls_link.click()

            # Aguarda o download ser concluído
            wait_for_download(download_dir)

            # Encontra o último arquivo baixado (o mais recente)
            list_of_files = glob.glob(f'{download_dir}/*.xls')  # Pode ajustar a extensão se necessário

            # Se precisar interagir com a página principal novamente
            driver.switch_to.default_content()

            # Aguarda um tempo para garantir que a ação tenha sido realizada
            time.sleep(5)

        except Exception as e:
            print(f"Ocorreu um erro no ano {ano}: {e}")
            continue  # Continua para o próximo ano no caso de erro

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

        # Extrai o ano do nome do arquivo
        ano = os.path.splitext(xls_file)[0].split('_')[-1]

        # Verifica se o valor é 'conIncentivadorMecenatoPorRegiaoUF'
        if df.iloc[0,0] == 'conIncentivadorMecenatoPorRegiaoUF':
            # Se for, substitui pelo ano
            df.iloc[0,0] = ano
            print(ano)

        # Adiciona a coluna 'ANO' ao DataFrame
        df['ANO'] = ano

        # Remove a extensão .xls do nome do arquivo e adiciona .csv
        csv_file = os.path.splitext(xls_file)[0] + '.csv'

        # Obtém o caminho completo para o arquivo .csv (no diretório csv_dir)
        # cria o diretorio se ele não existir
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        csv_path = os.path.join(csv_dir, csv_file)

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
        df['ANO'] = df['ANO'].replace('conIncentivadorMecenatoPorRegiaoUF', 1993)

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
