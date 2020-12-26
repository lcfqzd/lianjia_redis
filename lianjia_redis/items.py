# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaRedisItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    addr = scrapy.Field()  # 地点

    price = scrapy.Field()  # 价格
    room = scrapy.Field()  # 厅室
    direc = scrapy.Field()  # 方向
    area = scrapy.Field()  # 面积
    agent = scrapy.Field()  # 经纪人

    model = scrapy.Field()  # 户型
    floor = scrapy.Field()  # 楼层
    type = scrapy.Field()  # 类型
    decorate = scrapy.Field()  # 装修
    elevayor = scrapy.Field()  # 电梯
    listedtime = scrapy.Field()  # 挂牌时间
    ownership = scrapy.Field()  # 交易权属
    use = scrapy.Field()  # 用途
    year = scrapy.Field()  # 年限
    moregage = scrapy.Field()  # 抵押

