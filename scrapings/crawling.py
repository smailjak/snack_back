import csv
import json

import requests
from bs4 import BeautifulSoup



CATEGORY_URLS = [
    'http://www.snackok.com/shop/shopbrand.html?type=X&xcode=001',
    'http://www.snackok.com/shop/shopbrand.html?type=X&xcode=002',
    'http://www.snackok.com/shop/shopbrand.html?type=X&xcode=003',
    'http://www.snackok.com/shop/shopbrand.html?type=X&xcode=004',
    'http://www.snackok.com/shop/shopbrand.html?type=X&xcode=005',
]

USER_AGENT = 'Mozilla/5.0'
HEADERS    = {'User-Agent': USER_AGENT}

def get_page_num(category_url):
    page = 4
    while True:
        common_category_url = f'{category_url}&sort=&page={page}'
        res  = requests.get(common_category_url, headers=HEADERS)
        data = BeautifulSoup(res.content, 'html.parser')
        if data.find('div', {'class': 'items'}) is None:
            break
        page += 1
    return page - 1

def get_urls_in_one_category(category_url):
    urls_in_one_category = []
    page_num = get_page_num(category_url)
    print(f'page_num:{page_num}')
    for page in range(page_num):
        urls_in_one_category.append(f'{category_url}&sort=&page={page+1}')
    return urls_in_one_category


def return_all():
    result = {}
    for category_url in CATEGORY_URLS:
        urls_in_one_category     = get_urls_in_one_category(category_url)
        products_in_one_category = []

        for url in urls_in_one_category: 
            res  = requests.get(url, headers=HEADERS)
            data = BeautifulSoup(res.content, 'html.parser')

            for product in data.select("dl.item"):
                price_strike = None if product.find('span', {'class': 'price-strike'}) is None else product.find('span', {'class': 'price-strike'}).text.replace("\n", "").replace("\\", "")
                price_red = None if product.find('span', {'class': 'price-red'}) is None else product.find('span', {'class': 'price-red'}).text.replace("\\", "")
                item_price = None if price_strike or price_red is not None else product.find('p', {'class': 'item-price'}).find('span').text.replace("\\", "")

                item = {
                    'img'          : product.find('img', {'class': 'MS_prod_img_s'}).get('src'),
                    'item_name'    : product.find('p', {'class': 'item-name'}).text,
                    'price-strike' : price_strike,
                    'price-red'    : price_red,
                    'item-price'   : item_price
                }
                products_in_one_category.append(item)
    
        f = csv.writer(open(f"{category_url[-5:]}.csv", "w"))

        f.writerow(['img', 'item_name', 'price-strike', 'price-red', 'item-price'])

        for product in products_in_one_category:
            f.writerow([product["img"],
                        product["item_name"],
                        product["price-strike"],
                        product["price-red"],
                        product["item-price"]])



        result_by_category_url = {category_url: products_in_one_category}

        result.update(result_by_category_url)

    return result

print(return_all())
