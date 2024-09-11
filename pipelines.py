# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector as mysql
from db import database

class SteamMarketplacePipeline:
    def __init__(self):
        self.db, self.cursor = database.create_connection()
    
    def process_item(self, item, spider):
        try:
            self.insert_record(item)
        except mysql.IntegrityError:
            self.update_record(item)
        
        return item
    
    def insert_record(self, record):
        query = "INSERT INTO items(game,item,type,listings,price,description,icon,url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        vals = (
            record.get("Game"),
            record.get("Item"),
            record.get("Type"),
            record.get("Listings"),
            record.get("Price"),
            record.get("Description"),
            record.get("Icon"),
            record.get("Product URL")
        )

        self.cursor.execute(query, vals)
        self.db.commit()
    
    def update_record(self, record):
        query = "UPDATE items SET listings=%s, price=%s, updated_at=CURRENT_TIMESTAMP() WHERE game=%s AND item=%s"
        vals = (
            record.get("Listings"),
            record.get("Price"),
            record.get("Game"),
            record.get("Item")
        )

        self.cursor.execute(query, vals)
        self.db.commit()
    
    def close_spider(self,spider):
        database.close_connection(self.cursor, self.db)
