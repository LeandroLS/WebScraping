from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector

def checkNoneTypePrice(arg):
    if(arg is not None):
        return arg.getText().replace("R$", "").strip()
    else:
        return None

def checkNoneTypeLink(arg):
    if(arg is not None):
        return arg
    else:
        return None

def checkNoneTypeLocal(arg):
    if(arg is not None):
        return arg.getText().strip()
    else:
        return None

def checkNoneTypeTitleEAno(arg):
    if(arg is not None):
        return arg.getText().strip().split('-')
    else:
        return [None, None]

def checkNoneTypeKmECilindrada(arg):
    if(arg is not None):
        km_e_cilindrada = arg.getText().strip().split('|')
        km = km_e_cilindrada[0].replace("km", "").strip()
        return km
    else:
        return [None, None]

def inserirMoto(moto):
    price = checkNoneTypePrice(moto.find('p', {'class':'OLXad-list-price'}))
    link = checkNoneTypeLink(moto.get('href'))
    local = checkNoneTypeLocal(moto.find('p', {'class':'detail-region'}))

    title_e_ano = checkNoneTypeTitleEAno(moto.find('h2', {'class':'OLXad-list-title mb5px'}))
    title = title_e_ano[0]
    ano = title_e_ano[1].strip()

    km = checkNoneTypeKmECilindrada(moto.find('p', {'class' : 'detail-specific'}))

    add_moto = "INSERT INTO scraping_data_pcx (ano, km, local, preco, title, url) VALUES (%s,%s,%s,%s,%s,%s)"
    moto = (ano, km, local, price, title, link)
    try:
        cursor.execute(add_moto, moto)
    except mysql.connector.Error as err:
        print('Não foi possível inserir a moto olx')


url = 'https://sp.olx.com.br/sao-paulo-e-regiao/autos-e-pecas/motos/honda/pcx?q=pcx&re=36&rs=34'
html = urlopen(url)
soup = BeautifulSoup(html.read(),"html5lib")
motos = soup.findAll('a', {'class' : 'OLXad-list-link'})

cnx = mysql.connector.connect(user='root', database='pcx_scraping', password="123456", host='127.0.0.1')
cursor = cnx.cursor()

for moto in motos:
    inserirMoto(moto)
    cnx.commit()

paginacao = soup.find('div', {'class' : 'module_pagination'})

if(paginacao is not None):
    links_list = []
    links = paginacao.findAll('a', {'class' : 'link'})
    for link in links:
        links_list.append(link.get('href'))

    for link in links_list:
        url = link
        html = urlopen(url)
        soup = BeautifulSoup(html.read(),"html5lib")
        motos = soup.findAll('a', {'class' : 'OLXad-list-link'})
        for moto in motos:
            inserirMoto(moto)
            cnx.commit()
           
         
