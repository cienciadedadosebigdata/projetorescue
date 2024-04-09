## Configurações do Selenium
## Importando biblioteca os para manipulação de diretórios
from prereqs import *

# Diretório para salvar os downloads
download_dir = "arquivos_salic/xls"
download_dir = os.path.abspath(download_dir)  # Converte para caminho absoluto se necessário
xls_dir = download_dir
csv_dir = "arquivos_salic/csv"
csv_final = "arquivos_salic/dados_salic.csv"

# Configuração das opções do Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,  # Para desativar a confirmação de download
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,  # Para desativar o aviso de segurança ao baixar arquivos
    "safebrowsing_for_trusted_sources_enabled": False,  # Para desativar a proteção contra phishing e malware
    "safebrowsing.disable_download_protection": True,  # Para desativar a proteção contra downloads inseguros
    "profile.default_content_setting_values.automatic_downloads": 1,  # Para permitir downloads automáticos
})

# Desativa os avisos de segurança do Chrome
chrome_options.add_argument("--safebrowsing-disable-extension-blacklist")
chrome_options.add_argument("--safebrowsing-disable-download-protection")
chrome_options.add_argument("--disable-web-security")  # Desativa a verificação de sites não seguros

# Inicializa o WebDriver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Maximiza a janela do navegador
driver.maximize_window()

# Define um tempo máximo de espera para os elementos serem encontrados
wait = WebDriverWait(driver, 10)