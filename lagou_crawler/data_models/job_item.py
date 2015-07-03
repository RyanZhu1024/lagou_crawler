# coding=utf-8

__author__ = 'shuxuan'


class JobItem:
    def __init__(self, name, salary, address, des, benefit, requirements):
        self.requirements = requirements
        self.name = name
        self.salary = salary
        self.address = address
        self.description = des
        self.benefits = benefit

    collection = 'job_items'