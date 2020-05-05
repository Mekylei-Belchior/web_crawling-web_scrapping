#!/usr/bin/python
# -*- coding: utf-8 -*-

### DOWNLOAD LIVROS GRATUÍTOS
#
# Fonte: Springer Nature Switzerland AG
# Criado em: 01/05/2020
#
# ATENÇÂO: Na data de criação deste código não havia restições
# quanto ao download das obras gratuídas. Utilize-o com responsabilidade! 
#
# INFO: Código baseado no script do Leandro Souza
# do grupo de WhatsApp (Amigos High Tech Brasil)

# Importando os pacotes
from os import path, mkdir, rename
from wget import download
from sys import stdout
import pandas as pd

# Carregados os dados no DataFrame
csv_file = 'https://raw.githubusercontent.com/Mekylei-Belchior/web_crawling-web_scrapping/master/Livros%20SPRING/url_books.csv'
books = pd.read_csv(csv_file)

# Verifica se no diretório corrente do arquivo (.py) existe o diretório (Springer)
# Caso não, cria o diretório
if not path.exists('Springer'):
    mkdir('Springer')

# Declaração de variáveis:
# i = contador
# total = total de livros no DataFrame 
i = 0
total = len(books)

print()

# Percorre todas as linha do DataFrame pelo índice
for index in books.index:
    # Incrementa o contador a cada interação do laço
    i += 1

    # Verifica se dentro do diretório (Springer) existe o diretório
    # (Springer/[área do livro]). Caso não, cria o diretório
    if not path.exists('Springer/' + books.loc[index][1]):
        mkdir('Springer/' + books.loc[index][1])

    # Obtém o nome do livro do índice atual
    book_name = books.loc[index][0]

    # Verifica se dentro do diretório Springer/[área do livro]/
    # existe o arquivo [nome do livro].pdf
	# Caso não, cria o arquivo
    if not path.exists('Springer/' + books.loc[index][1] + '/' + book_name + '.pdf'):
        print()
        print(f'\033[1;33mDownloading Now :\033[m \033[1;36m{book_name}\033[m')

        # Faz o download do arquivo com o nome de origem
        filename = download(books.loc[index][2], out='Springer/' + books.loc[index][1])
        # Define o novo nome do arquivo
        save_file_as = 'Springer/' + books.loc[index][1] + '/' + book_name + '.pdf'
        # Renomeia o arquivo baixado
        rename(filename, save_file_as)

    # Imprime no terminal os dados de download
    stdout.write('\r%s%d%s\n' % (
    	'\033[1;32mStatus download books\033[m [ ',
    	int(round(float(i)/total*100)), 
    	'% ] ['
    	)
    ) 
    print() 
    stdout.flush()
