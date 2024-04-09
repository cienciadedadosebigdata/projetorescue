## Importando bibliotecas e configurações necessárias:
from prereqs import *
from functions import *
from conf_selenium import *

# Busca os XLs no site do SALIC
processa_anos(1993, 1995)

# Fecha o navegador
driver.quit()

# Converter e mover os arquivos
converte_xls_para_csv("arquivos_salic")