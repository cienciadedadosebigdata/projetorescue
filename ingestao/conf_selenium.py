## Configurações do Selenium
## Importando biblioteca os para manipulação de diretórios
from prereqs import *

# Diretório para salvar os downloads
download_dir = "arquivos_salic"
download_dir = os.path.abspath(download_dir)  # Converte para caminho absoluto se necessário

# Configuração das opções do Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,  # Para desativar a confirmação de download
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Inicializa o WebDriver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Maximiza a janela do navegador
driver.maximize_window()

# Define um tempo máximo de espera para os elementos serem encontrados
wait = WebDriverWait(driver, 10)