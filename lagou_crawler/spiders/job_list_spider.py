# coding=utf-8

from scrapy import Spider
import scrapy

from lagou_crawler.data_models.job_source import JobSource
from lagou_crawler.data_storage import mongo_store


__author__ = 'shuxuan'


# a spider for lagou.com to all jobs profile from every category to save in job sources
class LagouSpider(Spider):
    name = "jobs"
    allowed_domains = ["lagou.com"]

    @staticmethod
    def build_url(keyword, page_num):
        utf8 = [u'http://www.lagou.com/jobs/list_'.encode('utf8'), keyword.encode('utf8'),
                u'?city=上海&pn='.encode('utf8'), str(page_num).encode('utf8')]
        return ''.join(utf8)

    def __init__(self):
        menu_items = mongo_store.find__menu_all_keywords()
        for item in menu_items:
            for keyword in item["keywords"]:
                link = self.build_url(keyword, 1)
                self.start_urls.append(link)

    start_urls = []


    def parse(self, response):
        # job_as = sel.xpath('//li[@data-jobid]/div[contains(@class,"hot_pos_l")]//a/@href').extract()
        job_divs = response.xpath('//li[@data-jobid]')
        temp_job_sources = []
        for job_div in job_divs:
            job_id = job_div.xpath('@data-jobid').extract()[0]

            job_link = job_div.xpath('.//div[contains(@class,"hot_pos_l")]//a/@href').extract()[0]
            job_source = JobSource(job_id, job_link)
            if mongo_store.find_by_job_id(job_source) is None:
                print job_source.job_id, job_source.link
                mongo_store.save(job_source)
                temp_job_sources.append(job_source)
        if len(temp_job_sources) > 0:
            try:
                page = int(response.url[-1]) + 1
                url = ''.join([response.url[:-1], str(page)])  # 变成整数，然后加上分页
                yield scrapy.Request(url, callback=self.parse)
            except ValueError:
                print "oooooooooooooooooooooooopssssssssssssssssss", response.url[-1]
                return
            finally:
                del temp_job_sources[:]
