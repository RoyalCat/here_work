import scrapy
from bs4 import BeautifulSoup
import re

from shopsparser.items import ShopItem


class BeelineSpider(scrapy.Spider):
    name = 'beeline'
    start_urls = ['https://beeline-tochki.ru/store']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        cites_urls = [url['href'] for url in soup.main.div.div.find_all("div")[2].div.find_all("a")]
        for city_url in cites_urls:
            yield response.follow(city_url, self.parse_city)

    def parse_city(self, response):
        city_soup = BeautifulSoup(response.text, 'lxml')
        a_list = [p.a for p in city_soup.find_all("p") if p.a is not None]
        store_urls = [a['href'] for a in a_list if a['href'].startswith('/store/')]
        for store_url in store_urls:
            yield response.follow(store_url, self.parse_store)

    def parse_store(self, response):
        store_soup = BeautifulSoup(response.text, 'lxml')
        properties_soup = store_soup.find_all("div", {"class": "store_property"})
        properties_dict = {}
        for prop in properties_soup:
            properties_dict[prop.find("div", {"class": "title"}).text[:-2]] = prop.find("div",
                                                                                        {"class": "value"}).text.strip()
        item = ShopItem()
        item['address'] = properties_dict['Местонахождение']
        item['email'] = properties_dict['Электронная почта']
        item['phone'] = properties_dict['Телефон']
        try:
            work_time = re.findall("[0-2][1-9]:[0-5][0-9]", store_soup.find_all("table", {"class": "gray_table"})[0].tr.td.text)
            item['open_time'] = work_time[0]
            item['close_time'] = work_time[1]
        except (KeyError, IndexError):
            pass
        yield item

