from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector

def checkTypeNonePrice(arg):
    if(arg is not None):
        return arg.getText().strip()
    else:
        return None
def checkTypeNoneLocal(arg):
    if(arg is not None):
        return arg.getText().strip()
    else:
        return None
def checkTypeNoneTitle(arg):
    if(arg is not None):
        return arg.getText().strip()
    else:
        return None
def checkTypeNoneLink(arg):
    if(arg is not None):
        return arg
    else:
        return None
def checkTypeNoneAnoEKm(arg):
    if(arg is not None):
        return arg.getText().split("|")
    else:
        return [None,None]

def InserirMoto(moto):
    price = checkTypeNonePrice(moto.find('span', {'class':'price__fraction'}))
    local = checkTypeNoneLocal(moto.find('div', 'item__location'))
    title = checkTypeNoneTitle(moto.find('span', 'main-title'))
    link = checkTypeNoneLink(moto.get('href'))
    
    ano_e_km = checkTypeNoneAnoEKm(moto.find('div', 'item__attrs'))
    ano = ano_e_km[0]
    km = ano_e_km[1]

    add_moto = "INSERT INTO scraping_data_pcx (ano, km, local, preco, title, url) VALUES (%s,%s,%s,%s,%s,%s)"
    moto = (ano, km, local, price, title, link)
    try:
        cursor.execute(add_moto, moto)
    except mysql.connector.Error as err:
        print('Não foi possível inserir a moto mercado livre')

cnx = mysql.connector.connect(user='root', database='pcx_scraping', password="123456", host='127.0.0.1')
cursor = cnx.cursor()

html = urlopen("https://motos.mercadolivre.com.br/scooters/honda/sao-paulo/usados/2016-2018/honda-pcx")
res = BeautifulSoup(html.read(),"html5lib")
motos = res.findAll("a", {"class":"item__info-link item__js-link "})

for index, moto in enumerate(motos):
    InserirMoto(moto)
    cnx.commit()

if (res.find('div', {'class' : 'pagination__container'}) is not None):
    paginacao = res.select("li[class='pagination__page']")
    link_paginacao = []
    
    for index, link in enumerate(paginacao):
        link_paginacao.append(link.a.get('href'))
    
    for link in link_paginacao:
        html = urlopen(link)
        res = BeautifulSoup(html.read(),"html5lib")
        motos = res.findAll("a", {"class":"item__info-link item__js-link "})
        for index, moto in enumerate(motos):
            InserirMoto(moto)
            cnx.commit()

print("Fim da busca.")
cursor.close()
cnx.close()    

