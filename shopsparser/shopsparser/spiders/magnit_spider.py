import re

import scrapy
from bs4 import BeautifulSoup

from shopsparser.items import ShopItem


class MagnitSpider(scrapy.Spider):
    name = 'magnit'
    start_urls = ['https://magnitcosmetic.ru/shops/shop_list.php']

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')
        cities_ids = [option['value'] for option in soup.find_all('select')[0].find_all('option')]
        for city_id in cities_ids:
            yield response.follow('https://magnitcosmetic.ru/shops/shop_list.php?city_id=' + city_id,
                                  callback=self.parse_city)

    def parse_city(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        shops_urls = [shop.a['href'] for shop in soup.find_all('div', {'class': 'shops__address'})]
        for shop_url in shops_urls:
            yield response.follow(shop_url, callback=self.parse_shop)

    def parse_shop(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = ShopItem()
        try:
            item['address'] = soup.find('h1', attrs={'class': 'shop__address'}).text.strip()
        except AttributeError:
            pass
        item['phone'] = soup.find('div', attrs={'class': 'phone__number'}).text.strip()

        try:
            work_time_s = soup.find('div', attrs={'class': 'shop-detail__time'}).text.strip()
            work_time = re.findall("[0-2][1-9]:[0-5][0-9]", work_time_s)
            item['open_time'] = work_time[0]
            item['close_time'] = work_time[1]
        except (KeyError, IndexError):
            pass
        yield item
