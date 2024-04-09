## Importando bibliotecas e configurações necessárias:
from prereqs import *
from functions import *
from conf_selenium import *

# Busca os XLs no site do SALIC
processa_anos(1993, 1995)

# Fecha o navegador
driver.quit()

# Converter e mover os arquivos
converte_xls_para_csv(xls_dir, csv_dir)

# Gera um csv único
unico_csv(csv_dir, csv_final)