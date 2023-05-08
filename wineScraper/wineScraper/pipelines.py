from itemadapter import ItemAdapter
import pymongo
from .items import WineItem

class WinescraperPipeline:
    collection = 'wine'
    
    def __init__(self):
        self.uri = 'mongodb://localhost:27017'
        self.db = 'wineDB'
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[self.db]
        self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        value = adapter.get('info')
        value = value.replace("\n", "")
        adapter['info'] = value

        # data = dict(item)
        # self.db[self.collection].insert_one(data)

        print(f"Processing item: {item}")

        try:
            self.db[self.collection].insert_one(dict(item))
            print(f"Inserted item into database: {item}")
        except Exception as e:
            print(f"Error inserting item into database: {e}")

        return item
