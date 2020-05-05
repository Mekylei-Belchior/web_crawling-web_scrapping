# -*- coding: utf-8 -*-

### DOWNLOAD LIVROS GRATUÍTOS ###
#
# Fonte dos livros: 
# Eduff - Editora da Universidade Federal Fluminense
# 
# Criado em 05/05/2020
# 
# ATENÇÂO: Na data de criação deste código não havia restições
# quanto ao download das obras gratuídas. Utilize-o com responsabilidade! 

# Importando os pacotes
from bs4 import BeautifulSoup as bfs
from os import path, mkdir, rename
from wget import download
from sys import stdout
from requests import get as get_page


# Lista com os caracteres não aceitáveis para nome de arquivo (Windows)
forbidden = [':', '|', '/', '<', '>', '*', '?', '"']

def text_clear(text):
  '''

  Remove os caracteres irregulares para nome de arquivo
  
  Arguments:
    text: string com o nome do arquivo
  
  Returns:
    Texto sem os caracteres irregulares

  '''
  
  # Obtém os caracteres irregulares contido no texto
  characters = [character for character in text if character in forbidden]

  # Aplica a função (replace) ao texto 
  # conforme a quantidade de caracteres irregulares encontrados
  for i in range(0, len(characters)):
      text = text.replace(characters[i], '')

  return text

# Página inicial
PAGE = 'http://www.eduff.uff.br/index.php/catalogo/e-books'

# Obtém os elementos HTML da página em forma de texto
html = get_page(PAGE)
html = html.text

# Converte para um documento HTML estruturado
soup = bfs(html, 'html.parser')
# Obtém os elemetros das tags aninhadas
tags = soup.select('li > div > a')

# Verifica se no diretório corrente do arquivo (.py)
# existe o diretório (Livros EDUFF). Caso não, cria o diretório
if not path.exists('Livros EDUFF'):
      mkdir('Livros EDUFF')

# Declaração de variáveis:
# i = contador
# total = quantidade de tags obtidas 
i = 0
total = len(tags)

for tag in tags:
  # Incrementa o contador a cada interação do laço
  i += 1

  # Executa o bloco se o conteúdo da tag (title)
  # for diferente de None
  if not tag.get('title') is None:
    # Obtém o título estruturado do livro 
    title = text_clear(tag.get('title'))
    # Obtém os elementos HTML da página em forma de texto
    html =  get_page('http://www.eduff.uff.br' + tag.get('href'))
    html = html.text
    # Converte para um documento HTML estruturado
    soup = bfs(html, 'html.parser')
    # Obtém o atributo (href) da tag (a)
    download_link = soup.select(
      '#content > div.item-page > div > div.span3.livros-ficha > a[href]')

    # Executa o bloco se a variável (download_link) não estiver vazia
    if len(download_link) > 0:
      link = download_link[0].get('href')

      # Executa o bloco se o arquivo não existir
      if not path.exists('Livros EDUFF/' + title + '.pdf'):
        print()
        msg = 'Downloading Now: '
        print(f'\033[1;33m{msg}\033[m\033[1;36m{title}\033[m')
        print(f'\033[1;33mLink:\033[m {link}')

        # Faz o download do arquivo
        filename = download(link, out='Livros EDUFF/' + title)
        # Define o nome do arquivo
        save_file_as = 'Livros EDUFF/' + title + '.pdf'
        # Renomeia o arquivo
        rename(filename, save_file_as)

        # Imprime no terminal os dados de download
        stdout.write(
          '\r[%s\n' % ('\033[1;32m Status book | download completed\033[m '))
        # Imprime no terninal a barra de progresso
        done = int(50 * i / total)
        stdout.write("\rProgress: [%s%s] %d%%" % ('\033[1;32m■\033[m' * done,
          ' ' * (50 - done),
          100 * i / total))

        print()
        stdout.flush()

    else:
      msg = 'WARNING: An error occurred while downloading the file book.'
      print(f'\n\033[1;31m{msg}\033[m {title}\nLink: {link}')
      continue
