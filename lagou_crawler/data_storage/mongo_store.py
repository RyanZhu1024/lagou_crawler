# coding=utf-8
from lagou_crawler.data_models.job_source import JobSource
from lagou_crawler.data_models.menu_items import MenuItem
from lagou_crawler.data_models.job_item import JobItem

__author__ = 'shuxuan'

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['lagou']


def save(model):
    model_collection = model.__class__.collection
    db_collection = db[model_collection]
    ele = dict()
    for key, value in model.__dict__.iteritems():
        ele[key] = value
    db_collection.insert_one(ele)


def find_by_job_id(model):
    model_collection = model.__class__.collection
    db_collection = db[model_collection]
    return db_collection.find_one({"job_id": model.job_id})


def find_job_detail_by_job_id(job_id):
    db_collection = db[JobItem.collection]
    return db_collection.find_one({"job_id": job_id})


def find__menu_all_keywords():
    return db[MenuItem.collection].find()


def find_job_all_urls():
    return db[JobSource.collection].find()
