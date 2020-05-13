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
HEADERS = {'User-Agent': USER_AGENT}

def get_page_num(category_url):
    page = 1
    while True:
        common_category_url = f'{category_url}&sort=&page={page}'
        res = requests.get(common_category_url, headers=HEADERS)
        data = BeautifulSoup(res.content.decode('euc-kr', 'replace'), 'html.parser')
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
        urls_in_one_category = get_urls_in_one_category(category_url)
        products_in_one_category = []
        for url in urls_in_one_category: 
            res = requests.get(url, headers=HEADERS)
            data = BeautifulSoup(res.content.decode('euc-kr', 'replace'), 'html.parser')

            items = data.find('div', {'class': 'items'})
            tbody = items.find('tbody')
            trs = tbody.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td')
                for product in tds:
                    item = {'item_name': product.find('p', {'class': 'item-name'}).text, 'next': 'next'}
                    products_in_one_category.append(item)
        result_by_category_url = {category_url: products_in_one_category}
        print(f'number_in_one_category: {len(products_in_one_category)}')
        result.update(result_by_category_url)
    return result

print(return_all())