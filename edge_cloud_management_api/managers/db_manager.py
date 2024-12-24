from pymongo import MongoClient
from edge_cloud_management_api.configs.env_config import Config


class MongoManager:
    def __init__(self):
        """
        Initializes the MongoDB connection using the URI from Config.
        """
        self.client = MongoClient(Config.MONGO_URI)
        mongo_db_name: str = Config.MONGO_URI.split("/")[-1]
        self.db = self.client[mongo_db_name]

    def insert_document(self, collection_name, document):
        """
        Inserts a document into the specified collection.
        """
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def find_document(self, collection_name, query):
        """
        Finds a single document based on the query.
        """
        collection = self.db[collection_name]
        return collection.find_one(query)

    def find_documents(self, collection_name, query):
        """
        Finds multiple documents based on the query.
        """
        collection = self.db[collection_name]
        return collection.find(query)

    def update_document(self, collection_name, query, update_data):
        """
        Updates a single document based on the query.
        """
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update_data})
        return result.modified_count

    def delete_document(self, collection_name, query):
        """
        Deletes a single document based on the query.
        """
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
