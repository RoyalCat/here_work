# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopItem(scrapy.Item):
    shop_name = scrapy.Field()
    open_time = scrapy.Field()
    close_time = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
