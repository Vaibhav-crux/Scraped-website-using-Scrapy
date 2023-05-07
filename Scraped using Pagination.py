import scrapy
import datetime
import json

class NoonSpider(scrapy.Spider):
    name = "noon"
    start_urls = ['https://www.noon.com/_svc/catalog/api/v3/u/all-p-fbn-ae/']
    def parse(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        print(data)
        category_data = data['facets'][1]['data']
        for code in category_data:
            children = code['children']
            for child in children:
                url = 'https://www.noon.com/_svc/catalog/api/v3/u/{}/?limit=200&page={}'
                page = response.body
                total_page=json.loads(page)
                nb_page = total_page['nbPages']
                for i in range(1, 31):
                    sub = child['code']
                    full_link = url.format(sub,i)
                    yield scrapy.Request(url=full_link,callback=self.parse_product)

    def parse_product(self,response):
        # yield {'response':response.url}
        data = json.loads(response.text)
        api_hits = data.get('hits')
        rank = 0
        for hit in api_hits:
            rank = rank + 1
            sku = hit.get('sku')
            sku_link = f"https://www.noon.com/_svc/catalog/api/v3/u/l/{sku}/p/"
            yield scrapy.Request(url=sku_link, headers={'x-locale': 'en-ae'},callback=self.parse_json,meta={'sku': sku,  'rank': rank})

    def parse_json(self, response):
        today = datetime.datetime.now()
        today = today.strftime("%b-%d-%Y %H:%M:%S")
        product = response.json()
        product['sku'] = response.meta.get('sku')
        product['page'] = response.meta.get('page')
        product['rank'] = response.meta.get('rank')
        product['date'] = today
        data = []
        data.append(product)
        yield {'product':data}
