import scrapy


class LianjiaRedisSpiderSpider(scrapy.Spider):
    name = 'lianjia_redis_spider'
    allowed_domains = ['xxx.com']
    start_urls = ['http://xxx.com/']

    def parse(self, response):
        pass
