from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd
import time


#Configuração para o driver do Chrome
def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Modo em que o chrome nao abre a janela no dispositivo
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#Acesssa a pagina principal com diversos notebooks a venda
def acessar_pagina_principal(driver, url):
    driver.get(url)
    time.sleep(5)

    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root-app"]/div/div[2]/section/div[7]/ol'))
        )
    except:
        driver.quit()
        exit()

#Coleta cada link de cada produto a venda na pagina principal
def coletar_links_produtos(product_list):
    links = list(set(
        el.get_attribute('href') for el in product_list.find_elements(By.TAG_NAME, 'a') if el.get_attribute('href')
    ))
    return links

#Extrai cada valor do item selecionado na lista de links
def extrair_dados(driver, url):
    driver.get(url)
    time.sleep(10)
    try:
        div_principal = driver.find_element(By.XPATH, '//*[@id="ui-pdp-main-container"]/div[1]/div/div[2]/div[2]')
    except:
        return None

    soup = BeautifulSoup(div_principal.get_attribute('outerHTML'), 'html.parser')
    try:
        descricao = soup.find("h1", class_="ui-pdp-title").get_text().strip()
        precos = soup.find_all("span", class_="andes-money-amount__fraction")
        preco_sem_desc = float(precos[0].get_text().replace(".", ""))
        preco_com_desc = float(precos[1].get_text().replace(".", "")) if len(precos) > 1 else None

        especificacoes = []
        specs_ul = soup.find("ul", class_="ui-vpp-highlighted-specs__features-list")
        if specs_ul:
            especificacoes = [li.get_text(strip=True) for li in specs_ul.find_all("li")]

        campos = {
            "Versão do sistema operacional": None,
            "Edição do sistema operacional": None,
            "Nome do sistema operacional": None,
            "Capacidade de disco": None,
            "Memória RAM": None,
            "Placa gráfica": None
        }

        for item in especificacoes:
            for chave in campos:
                if chave in item:
                    campos[chave] = item.split(":", 1)[1].strip()

        return {
            'Descrição': descricao,
            'Preço Sem Desconto': preco_sem_desc,
            'Preço Com Desconto': preco_com_desc,
            'Versão do SO': campos["Versão do sistema operacional"],
            'Edição': campos["Edição do sistema operacional"],
            'Nome do SO': campos["Nome do sistema operacional"],
            'Armazenamento': campos["Capacidade de disco"],
            'Memoria Ram': campos["Memória RAM"],
            'Placa Gráfica': campos["Placa gráfica"],
            'URL': url
        }

    except Exception as e:
        return None

#Salva os dados em um Dataframe para um excel
def salvar_excel(dados):
    df = pd.DataFrame(dados)
    nome_arquivo = 'notebooks_preco.xlsx'
    df.to_excel(nome_arquivo, index=False)


def main():
    driver = setup_driver()
    url = 'https://lista.mercadolivre.com.br/notebook#topkeyword'
    lista_produtos = acessar_pagina_principal(driver, url)
    links = coletar_links_produtos(lista_produtos)

    dados = []
    for _, link in enumerate(links, 1):
        resultado = extrair_dados(driver, link)
        if resultado:
            dados.append(resultado)

    driver.quit()
    salvar_excel(dados)

if __name__ == "__main__":
    main()