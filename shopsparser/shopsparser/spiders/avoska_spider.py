import scrapy
from bs4 import BeautifulSoup

from shopsparser.items import ShopItem


class AvoskaSpider(scrapy.Spider):
    name = 'avoska'
    start_urls = ['https://avoska.ru/api/get_shops.php']

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')
        shops_list = [x.contents[0] for x in soup.find_all("li")]
        for shop in shops_list:
            item = ShopItem()
            item['address'] = shop
            yield item
