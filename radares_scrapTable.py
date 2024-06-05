from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller
import os
import pandas as pd
from bs4 import BeautifulSoup


# PASTA PARA SALVAR OS DADOS
DADOS_DIR = os.getcwd() + "\dados" # pasta atual do projeto
#TODO: usar arquivo de configuração para definir a pasta de download


# Configurando o WebDriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage') # avoid memory leak

# definindo o caminho para chromedriver de acordo com configuração do SO
chromedriver_autoinstaller.install()

# configura o webdriver
navegador = webdriver.Chrome(options=chrome_options)

# URL da página alvo
url = "https://servicos.dnit.gov.br/multas/informacoes/equipamentos-fiscalizacao"

# Obtendo o conteúdo da página
print("Acessando a página: ", url)
navegador.get(url)
print(navegador.title)

# Esperar até que o botão "Mostrar Tabela" esteja disponível e clicar
# CSS.SELECTOR: #app > div:nth-child(3) > div.wrapper-body.py-4 > div > div:nth-child(2) > div > div > button
print("Clicando no botão 'Mostrar Tabela'")
bt_mostrar_tabela = WebDriverWait(navegador, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div:nth-child(3) > div.wrapper-body.py-4 > div > div:nth-child(2) > div > div > button"))
)
bt_mostrar_tabela.click()

# Esperar até que a tabela seja carregada na página
# CSS.SELECTOR: #app > div:nth-child(3) > div.wrapper-body.py-4 > div > div.table-editais.table-responsive.mb-3 > table
tabela = WebDriverWait(navegador, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(3) > div.wrapper-body.py-4 > div > div.table-editais.table-responsive.mb-3 > table'))
)
print("Tabela carregada")


# BeautifulSoup
tabela_html = tabela.get_attribute('outerHTML')
soup = BeautifulSoup(tabela_html, 'html.parser')

headers = soup.find_all('th')[:-1] # ignorar a última coluna
colunas = [header.text for header in headers]

linhas = soup.find_all('tr')[1:] # ignorar a primeira linha (cabeçalho)
lista_de_itens = []
for item in linhas: # ignorar a primeira linha (cabeçalho)
    dados = item.find_all('td')[:-1] # ignorar a última coluna
    lista_de_itens.append([dado.text for dado in dados])

df = pd.DataFrame(lista_de_itens, columns=colunas)

# Salvar a tabela em um arquivo CSV
df.to_csv(DADOS_DIR + "\\radares.csv", index=False)
print("Tabela salva em: ", DADOS_DIR + "radares.csv")


# Fechar o navegador
navegador.quit()







