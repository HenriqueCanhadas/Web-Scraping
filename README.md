# 🛍️ Web Scraper de Notebooks no Mercado Livre

Este projeto é um **Web Scraper** desenvolvido em Python que coleta informações detalhadas sobre **notebooks à venda no site Mercado Livre**. Ele utiliza **Selenium** para automação de navegação e **BeautifulSoup** para extração de dados. Os resultados são armazenados em um arquivo `.xlsx`.

---

## 🚀 Funcionalidades

- Acessa automaticamente a página principal de notebooks no Mercado Livre
- Rola a página para carregar diversos produtos
- Extrai dados detalhados de cada produto:
  - Descrição
  - Preço (com e sem desconto)
  - Especificações técnicas (RAM, Armazenamento, Placa Gráfica, etc.)
- Exporta os dados para um arquivo Excel (`notebooks_preco.xlsx`)

---

## 🧰 Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [pandas](https://pandas.pydata.org/)
- [webdriver_manager](https://pypi.org/project/webdriver-manager/)
