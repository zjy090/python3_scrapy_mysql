# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class ScrapyMysqlPipeline(object):
    def getConnection(self):
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'database': 'wx',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }
        connection = pymysql.connect(**config)
        return connection

    # pipeline默认调用
    def process_item(self, item, spider):
        connection = self.getConnection()
        try:
            with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = "insert into spider_test(name,url,icon,date) values(%s,%s,%s,%s)"
                params = (item["name"], item["url"], item["icon"], item["date"])
                cursor.execute(sql, params);
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
        finally:
            connection.close()
