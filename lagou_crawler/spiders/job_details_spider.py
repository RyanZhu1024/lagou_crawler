# coding=utf-8
import operator

from lagou_crawler.data_models.job_item import JobItem
from lagou_crawler.data_storage import mongo_store


__author__ = 'shuxuan'

from scrapy import Spider


class JobDetailsSpider(Spider):
    name = "details"

    def __init__(self):
        job_urls = mongo_store.find_job_all_urls()
        for item in job_urls:
            job_id = item["job_id"]
            if mongo_store.find_job_detail_by_job_id(job_id) is None:
                self.start_urls.append(item["link"])

    start_urls = []

    def parse(self, response):
        if response.status == 200:
            title = response.xpath('//dt[contains(@class,"clearfix join_tc_icon")]//h1/@title').extract()[0]
            job_id = response.xpath('//input[contains(@id,"jobid")]/@value').extract()[0]
            job_request = response.xpath('//dd[contains(@class,"job_request")]//span/text()').extract()
            job_other_ben = response.xpath('//dd[contains(@class,"job_request")]/text()').extract()
            job_des = response.xpath('//dd[contains(@class,"job_bt")]//p/text()').extract()
            job_address = response.xpath('//dl[contains(@class,"job_company")]//div/text()').extract()[2]
            job_benefits = job_other_ben[-2].strip()
            job_benefits_arr = job_benefits[operator.indexOf(job_benefits, ":") + 1:].split(u"、")
            job_item = JobItem(title, job_request[0], job_address.strip(), job_des, job_benefits_arr, job_request[1:],
                               response.url, job_id)
            mongo_store.save(job_item)