import pymongo.errors

import model
from pymongo import MongoClient


class StorageMongoDb(model.BaseStorage):
    def __init__(self, conn_str: str, db_name: str, collection_name: str = ""):
        self.client = MongoClient(conn_str)
        self.db = self.client[db_name]
        self.collection_name = collection_name
        if collection_name != "":
            self.collection = self.db[collection_name]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()

    def save(self, item: model.BaseItem, collection_name: str = ""):
        doc = item.to_dict()
        if doc["id"] != "":
            doc["_id"] = doc["id"]
        del doc["id"]
        try:
            if collection_name == "" or collection_name == self.collection_name:
                self.collection.insert_one(doc)
            else:
                self.db[collection_name].insert_one(doc)
        except pymongo.errors.DuplicateKeyError:
            pass
