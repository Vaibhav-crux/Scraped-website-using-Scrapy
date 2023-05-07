import scrapy

class MySpider(scrapy.spiders.SitemapSpider):
    name = 'noon' # Crawler name
    sitemap_urls = ['https://noon-sitemap.storage.googleapis.com/sitemap-index.xml'] # sitemap link
    sitemap_follow = ['categories'] # Those links which contains categories are crawled
    custom_settings = {
        'FEEDS': {'data.csv': {'format': 'csv', }} #Saving to csv file
    }

    def parse(self, response):
        name = response.css('div.cYgkvD span::text').get() # fetch Name of product
        cost = response.css('strong.amount::text').get() # fetch cost of product
        ratings = response.css('span.cmvYOR::text').get() # fetch ratings of product
 
        yield {
            'product_name': name,
            'product_cost': cost,
            'product_rating': ratings
        }
