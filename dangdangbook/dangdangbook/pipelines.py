# -*- coding: utf-8 -*-


class DangdangbookPipeline(object):
    def open_spider(self, spider):
        print("opened")

    def close_spider(self, spider):
        print("closed")

    def process_item(self, item, spider):
        print(item['title'])
        print(item['author'])
        print(item['publisher'])
        print(item['date'])
        print(item['price'])
        print(item['detail'])
        print()
        return item
