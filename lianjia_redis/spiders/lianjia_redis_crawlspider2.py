import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from ..items import LianjiaRedisItem


class LianjiaRedisSpider2Spider(CrawlSpider):
    name = 'lianjia_redis_crawlspider2'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://cq.lianjia.com/ershoufang/yubei/pg1/']

    # redis_key = 'lianjia_redis:start_urls'  # 可以被共享的调度器队列的名称
    # 稍后我们是需要将一个起始的url手动的添加到redis_key表示的队列中

    link = LinkExtractor(allow=r'/ershoufang/yubei/pg\d+')

    rules = (
        # 解析每一个页码对应页面中的数据
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath('//*[@id="content"]/div[1]/ul/li')
        print(li_list)
        for li in li_list:
            item = LianjiaRedisItem()

            title = li.xpath('./div[1]/div[1]/a/text()').extract_first()
            addr = li.xpath('./div[1]/div[2]/div//text()').extract_first()
            detail_url = li.xpath('./div[1]/div[1]/a/@href').extract_first()

            item['title'] = title
            item['addr'] = addr

            # 对每一个详情页发送请求
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        # 从meta中获取传递过来的item
        item = response.meta['item']
        item['price'] = response.xpath('/html/body/div[5]/div[2]/div[3]/span//text()').get() + '万'
        item['room'] = response.xpath('/html/body/div[5]/div[2]/div[4]/div[1]/div[1]/text()').get()
        item['direc'] = response.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/div[1]/text()').get()
        item['area'] = response.xpath('/html/body/div[5]/div[2]/div[4]/div[3]/div[1]/text()').get()
        item['agent'] = response.xpath('//*[@id="zuanzhan"]/div[2]/div/div[1]/a/text()').get()

        item['model'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()').get()
        item['floor'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()').get()
        item['type'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[6]/text()').get()
        item['decorate'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()').get()
        item['elevayor'] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()').get()
        item['listedtime'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/span[2]/text()').get()
        item['ownership'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()').get()
        item['use'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[4]/span[2]/text()').get()
        item['year'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[5]/span[2]/text()').get()
        item['moregage'] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()').get()

        yield item
