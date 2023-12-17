import psycopg2
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
import logging

class MashreghNewsPipeline:
    def process_item(self, item, spider):
        return item


class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = psycopg2.connect(database="saeed",
                        host="172.17.0.2",
                        user="saeed",
                        password="saeed",
                        port="5432")
        self.connection.autocommit=True
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute('''INSERT INTO NEWS(URL,TITLE, TEXT, IMG,NEWS_DATE ) VALUES (%s,%s,%s,%s,%s)''',
                                (item['url'],item['title'],item['text'], item['image'],datetime.now()))
            return item
        except BaseException as e:
            logging.error('Error In SavingToPostgresPipeline: %s', e)
            self.connection.commit        

class DuplicateNewsPipeline:
    
    def __init__(self):
        self.seen_url = set()

    def process_item(self,item,spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.seen_url:
            raise DropItem(f"Duplicate Item Found: {item!r}")   
        else:
            self.seen_url.add(adapter['title'])
            return item
