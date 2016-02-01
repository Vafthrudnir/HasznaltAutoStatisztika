# -*- coding: utf-8 -*-

from lxml import html
from lxml.etree import tostring
import requests
from BeautifulSoup import BeautifulSoup
import re
import matplotlib

brand = "mazda"
model = "3"

header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
url_base = "http://www.hasznaltauto.hu/auto/" + brand + "/" + model + "/"

page = requests.get(url_base, headers=header)
tree = html.fromstring(page.content)

num_of_pages = int(tree.xpath('//*[@class="oldalszam"][last()]')[0].text)

database = []

for i in range(num_of_pages):
    print i + 1, "/", num_of_pages

    url = url_base + "page" + str(i+1)
    page = requests.get(url, headers=header)
    tree = html.fromstring(page.content)

    prices = tree.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " arsor ")]')
    years = tree.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " talalati_lista_infosor ")]')
    for idx, price in enumerate(prices):
        try:
            price_string = price[0].text[:-3]
        except IndexError:
            print "Ar nelkul"
            continue
        try:
            act_price = int(re.sub("\.", '', price_string))
        except ValueError:
            print "Akcios"
            continue
        soup = BeautifulSoup(tostring(years[idx]))
        pattern = "(\d{4}|\d{4}\/\d*)&#160;"
        act_year = re.findall(pattern, soup.text)[0]

        database += [(act_year, act_price)]

for item in database:
    print item