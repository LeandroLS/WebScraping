from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://store.steampowered.com/search/?filter=globaltopsellers&os=win")
res = BeautifulSoup(html.read(),"html5lib")
titleGame = res.findAll("div", {"class":"responsive_search_name_combined"})

no_discount_class = 'col search_price responsive_secondrow'
discount_class = 'col search_price discounted responsive_secondrow'

for index, title in enumerate(titleGame):
    name = title.span.getText()
    if(title.find('div', 'col search_price responsive_secondrow') is not None):
        no_discount_price = title.find('div', no_discount_class).getText().strip()
        print("Nº {0} {1} {2}".format(index+1, name, no_discount_price))
    else:
        no_discount_price = title.find('div', discount_class).span.getText().strip()
        discount_price = title.find('div', discount_class)
        discount_price.span.decompose()
        discount_price = discount_price.getText().strip()
        print("Nº {0} {1} {2} {3}".format(index+1, name, no_discount_price, discount_price))
