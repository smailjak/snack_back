import requests
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent}

res = requests.get('http://www.snackok.com/shop/shopbrand.html?type=X&xcode=004', headers=headers)
data = BeautifulSoup(res.content.decode('euc-kr', 'replace'), 'html.parser')

items = data.find('div', {'class': 'items'})
tbody = items.find('tbody')
trs = tbody.find_all('tr')

product_num = 1
for tr in trs:
    tds = tr.find_all('td')
    for product in tds:
        print(product_num)
        product_num += 1
        item_name = product.find('p', {'class': 'item-name'}).text
        print(item_name)
