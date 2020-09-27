# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import requests
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ShopsparserPipeline:
    geocode_url = "https://geocode.search.hereapi.com/v1/geocode"
    api_key = 'Mftz7RERBmrGoqG8fpYgURwrc8byiAvre3mkJJ6D9yI'

    def get_coord(self, location: str):
        PARAMS = {'apikey': self.api_key, 'q': location}
        r = requests.get(url=self.geocode_url, params=PARAMS)
        data = r.json()
        if len(data['items']) > 0:
            return data['items'][0]['position']
        else:
            return None

    def process_item(self, item, spider):
        if item.get('address'):
            position = self.get_coord(item['address'])
            if position is not None:
                item['latitude'] = position['lat']
                item['longitude'] = position['lng']

            return item
        else:
            raise DropItem("Missing address")
