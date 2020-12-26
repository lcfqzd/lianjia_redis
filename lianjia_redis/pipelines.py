# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import redis
import pymongo
from pymysql import connect

from openpyxl import Workbook

# 创建工作薄Workbook
book = Workbook()

# 创建工作表Sheet
sheet = book.create_sheet('链家-重庆渝北二手房', 0)

# 向工作表中添加数据
sheet.append(
    ['标题', '地点', '价格', '厅室', '方向', '面积', '经纪人', '户型', '楼层', '类型', '装修', '电梯', '挂牌时间', '交易权属', '用途', '年限', '抵押'])


# 存储数据到Excel

class LianjiaRedisPipeline:
    # def open_spider(self, spider):
    #     pass

    def process_item(self, item, spider):
        row = [item['title'], item['addr'], item['price'], item['room'],
               item['direc'], item['area'], item['agent'], item['model'],
               item['floor'], item['type'], item['decorate'], item['elevayor'],
               item['listedtime'], item['ownership'], item['use'], item['year'],
               item['moregage']
               ]
        sheet.append(row)

        # 输出保存
        book.save('重庆渝北二手房.xls')

        return item

    # def close_spider(self, spider):
    #     pass



class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()

    def process_item(self, item, spider):
        self.client.room.lianjia.insert_one(dict(item))

        return item

    def close_spider(self, spider):
        self.client.close()




class MysqlPipeline(object):
    def open_spider(self, spider):
        self.client = connect(host='localhost', port=3306, user='root', password='root', db='spiders', charset="utf8")
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        args = [item["title"],item["addr"],item["price"], item["room"],
                item["direc"],item["area"],item["agent"],item["model"],
                item["floor"],item["type"],item["decorate"],item["elevayor"],
                item['listedtime'],item['ownership'],item['use'],item['year'],
                item["moregage"]]

        sql = 'insert into t_lianjia VALUES (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql, args)
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()