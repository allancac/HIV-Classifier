from pymongo import MongoClient
from Configurations import Configurations


class TweetsDatabse(object):
    def __init__(self):
        self.database_conf = Configurations.load_database()
        self.client = MongoClient(self.database_conf["host"], self.database_conf["port"])
        database_name = self.database_conf["database_name"]
        collection_name = self.database_conf["collection_name"]
        self.db = self.client[database_name]
        self.colecao = self.db[collection_name]

    def insert_tweets(self, documentos, search_id):

        for doc in documentos:
            doc["request_id"].append(search_id)
            # pegar doc id
            obj = self.colecao.find_one({"_id": doc["_id"]})
            if obj:
                obj["request_id"].append(search_id)
                self.update_search(obj, ["request_id"])
                continue
            else:
                self.colecao.insert_one(doc)

    def update_search(self, doc, list_update=None):
        key = {"_id": doc["_id"]}
        update = {"$set": {}}
        for tag in list_update:
            update["$set"][tag] = doc[tag]

        self.colecao.update_one(key, update)

    def getTwitter(self, id):
        key = {"_id": id}
        obj = self.colecao.find_one(key)
        if obj:
            return obj
        else:
            print("Não encontrado")


class SearchDatabase(object):
    def __init__(self):
        self.database_conf = Configurations.load_database()
        self.client = MongoClient(self.database_conf["host"], self.database_conf["port"])
        database_name = self.database_conf["database_name"]
        self.db = self.client[database_name]
        collection_name = self.database_conf["search_database_name"]
        self.colecao = self.db[collection_name]

    def insert_search(self, doc):
        self.colecao.insert_one(doc)

    def update_search(self, doc, list_update=None):
        key = {"_id": doc["_id"]}
        update = {"$set": {}}
        for tag in list_update:
            update["$set"][tag] = doc[tag]

        self.colecao.update_one(key, update)
