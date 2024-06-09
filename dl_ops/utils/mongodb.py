import os
import sys
import yaml
import pymongo
import logging

class MongoDBClient:
    def __init__(
            self,
            db_params=None,
            user=None, passwd=None, server=None, database_name=None, tgt_collection_name=None,
    ):  
        
        self.user = user
        self.passwd = passwd
        self.server = server
        self.database_name = database_name
        self.tgt_collection_name = tgt_collection_name

        if not db_params is None:
            self.user = db_params['user']
            self.passwd = db_params['passwd']
            self.server = db_params['server']
            self.database_name = db_params['database_name']
            self.tgt_collection_name = db_params['tgt_collection_name']

        self.connect_to_db()

    def connect_to_db(self):
        print(f'connecting to MongoDB at {self.server} as {self.user}')
        self.tgt_collection, suc = self.setupMongoDB()
        print(f'Connection to MongoDB established Successfully !')

    def init_auth(self):
        """
        Initialize MongoDB authentication using the provided auth file.

        This function reads and parses the MongoDB authentication information from the specified YAML auth file.
        It extracts the username ('u') from the file content and returns it for use in MongoDB authentication.

        Args:
            auth_file (str): Path to the YAML authentication file containing MongoDB authentication information.

        Returns:
            str: The extracted MongoDB username from the auth file.

        Raises:
            SystemExit: If the auth file is not found or if there is an issue loading or parsing the file.
        """
                
        try:       
            self.USER = self.user
            self.PASSWD = self.passwd
            self.SERVER = self.server
            
        except yaml.YAMLError as exc:
            logging.warning("MongoDB could not load authentication file")
            exit(1)  

    def setupMongoDB(self):

        tgt_collection = None
        suc = False
        try:
            self.init_auth()
            mongo_client = pymongo.MongoClient("mongodb://"+self.USER+":"+self.PASSWD+"@"+self.SERVER)
            db = mongo_client[self.database_name]
            tgt_collection = db[self.tgt_collection_name]
            suc = True
        except Exception as err:
            logging.warning('Error setting up MongoDB: %s !!! ❌' %err)

        return tgt_collection, suc
    
    def query(self, query):
        result = None
        count = 0
        try:
            result = self.tgt_collection.find(query)
            count = self.tgt_collection.count_documents(query)
        except Exception as err:
            logging.error('Error querying data from Mongo: %s' %err)

        return count, result
    
    def save_results_to_mongo(self, results):
        """
        Save processing results to a MongoDB collection.

        This function inserts the provided processing results into a specified MongoDB collection.
        After the insertion is complete, the MongoDB client connection is closed.

        Args:
            results (dict): A dictionary containing the processing results to be saved.

        Returns:
            None: The function inserts the results into the collection and closes the MongoDB client connection.
        """
        # Insert the results into the collection
        self.tgt_collection.insert_one(results)
