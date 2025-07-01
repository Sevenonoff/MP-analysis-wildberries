import time
import requests
from bs4 import BeautifulSoup
import sqlite3


conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# парсинг ВБ
def parse_wildberries(query, start_col=0, start_row=2):
    Geo = '2,12,7,3,6,13,21' 
    couponsGeo = '2,12,7,3,6,13,21'  
    dest = '-1113276,-77687,-398407,-1581689'  
    sort = 'popular'  # popular priceup rate newly benefit
    xsubject = '&xsubject=291'  
    xsubject = ''

    print(f"WB search query = {query}")
    url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo={couponsGeo}&curr=rub&dest={dest}&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query={query}&reg=0&regions=80,64,58,83,4,38,33,70,82,69,86,30,40,48,1,22,66,31&resultset=catalog&sort={sort}&spp=0&suppressSpellcheck=false{xsubject}'

    try:
        r = requests.get(url).json()
    except:
        print("Request exception in get_search_cards. Geo=" + Geo + "; url=" + url)
        for i in range(5):
            print("Trying to repeat: " + str(i))
            time.sleep(1)
            try:
                r = requests.get(url).json()
                print("Try " + str(i) + "success.")
                break
            except:
                print("Try " + str(i) + "fail.")

    print(len(r))
    line = 2
    if "data" in r:
        products = []
        for item in r['data']['products']:
            name = item['name']
            price = float(item['priceU'])/100
            discounted_price = float(item['salePriceU'])/100
            rating = float(item['reviewRating'])
            reviews_count = int(item['nmFeedbacks'])
            products.append((name, price, discounted_price, rating, reviews_count))

        return products

# cохранение данных в базу 
def save_to_db(products):

    cursor.executemany('''
    INSERT INTO products (name, price, discounted_price, rating, reviews_count)
    VALUES (?, ?, ?, ?, ?)
    ''', products)
    conn.commit()
