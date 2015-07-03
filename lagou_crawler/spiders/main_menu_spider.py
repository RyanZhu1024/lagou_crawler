# coding=utf-8

__author__ = 'shuxuan'

from scrapy import Spider

from lagou_crawler.data_storage import mongo_store
from lagou_crawler.data_models.menu_items import MenuItem


# a spider for lagou.com to get shanghai java with 30 pages, statically got


class LagouSpider(Spider):
    name = "main_menu"
    allowed_domains = ["lagou.com"]

    start_urls = [
        'http://www.lagou.com',
    ]

    job_ids_set = set()

    def parse(self, response):
        # job_as = sel.xpath('//li[@data-jobid]/div[contains(@class,"hot_pos_l")]//a/@href').extract()
        for menu_div in response.xpath('//div[contains(@id,"sidebar")]//div[contains(@class,"menu_box")]'):
            category = menu_div.xpath('.//div[contains(@class,"menu_main")]//h2/text()').extract()
            menu_item = MenuItem(category[0].strip())
            for keyword in menu_div.xpath('.//div[contains(@class,"menu_sub dn")]//dd//a/text()'):
                kw = keyword.extract()
                if kw.strip() is not "":
                    menu_item.keywords.append(kw.strip())

            mongo_store.save(menu_item)