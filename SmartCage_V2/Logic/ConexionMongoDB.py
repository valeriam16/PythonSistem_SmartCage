from pymongo import MongoClient


class ConexionMongoDB:
    def __init__(self, collection_name):
        uri = "mongodb+srv://admin:valeria16@myatlasclusteredu.njl6yr2.mongodb.net/?retryWrites=true&w=majority"
        database_name = 'sistema_de_cine'
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_document(self, document):
        self.collection.insert_one(document)

    def update_document(self, query, new_values):
        self.collection.update_one(query, {"$set": new_values})

    def delete_document(self, query):
        self.collection.delete_one(query)
