# coding=utf-8

__author__ = 'shuxuan'


class JobItem:
    def __init__(self, name, salary, address, des, benefit, requirements, url, job_id):
        self.requirements = requirements
        self.name = name
        self.salary = salary
        self.address = address
        self.description = des
        self.benefits = benefit
        self.url = url
        self.job_id = job_id

    collection = 'job_items'