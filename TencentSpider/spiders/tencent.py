# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TencentSpider.items import TencentspiderItem

class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parseContent', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
    def parseContent(self,response):
        for each in response.xpath('//tr[@class="even"|//tr[@class="odd"]'):
            item = TencentspiderItem()
            # 职位名
            item['positionname'] = each.xpath('./td[1]/a/text()').extract()[0]
            # 职位链接
            item['positionlink'] = each.xpath('./td[1]/a/@href').extract()[0]
            # 职位类型
            positiontype = each.xpath('./td[2]/text()').extract()
            # 职位类别可能为空
            if positiontype:
                item['positiontype'] = positiontype[0]
            else:
                item['positiontype'] = '职位类别'

            # 招聘人数
            item['peoplenumber'] = each.xpath('./td[3]/text()').extract()[0]
            # 工作地点
            item['worklocatiom'] = each.xpath('./td[4]/text()').extract()[0]
            # 发布时间
            item['publishtime'] = each.xpath('./td[5]/text()').extract()[0]

            yield item