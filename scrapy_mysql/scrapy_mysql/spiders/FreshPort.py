import scrapy
import tool
from scrapy_mysql.items import ScrapyMysqlItem
from scrapy.http import Request


class FreshPortSpider(scrapy.Spider):
    name = "FreshPort"
    allowed_domains = ['www.guojiguoshu.com']
    start_urls = ['http://www.guojiguoshu.com/news']

    def __init__(self):
        self.tool = tool.Tool()
        self.pageSize = 2
        self.baseUrl = 'http://www.guojiguoshu.com/news'

    # 解析页面并获取下一页继续
    def parse(self, response):
        post_nodes = response.xpath(
            '//div[re:test(@class, "view view-frontpage view-id-frontpage*")]//div[@class="content-list"]')
        for post_node in post_nodes:
            newsURL = post_node.xpath('a/@href').extract()
            print("新闻地址:" + newsURL[0])
            # print("新闻图片地址:" + div.a.img['src'])
            iconURL = post_node.xpath('a/img/@src').extract()
            print("新闻图片地址:" + iconURL[0])
            # print("新闻标题:" + self.tool.replace(div.div.a.text))
            titles = post_node.xpath('div/a/text()').extract()
            print("新闻标题:" + titles[0])
            # texts = list(div.div.strings)
            texts = post_node.xpath('div//text()').extract()
            print("新闻日期:" + self.tool.replace(texts[2]))
            # 转化成对象 并返回  这里很重要 返回会触发process_item
            yield self.parseDetail(newsURL[0], iconURL[0], titles[0], self.tool.replace(texts[2]))

        # 获取下一页并交给scrapy下载
        for i in range(1, self.pageSize):
            next_url = self.baseUrl + '?page=' + str(i)
            yield Request(url=next_url, callback=self.parse)

    def parseDetail(self, newsURL, iconURL, title, date):
        freshPort_item = ScrapyMysqlItem()
        freshPort_item['name'] = title
        freshPort_item['url'] = newsURL
        freshPort_item['icon'] = iconURL
        freshPort_item['date'] = date
        return freshPort_item
