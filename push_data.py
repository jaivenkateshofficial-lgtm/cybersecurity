import os
import json
import sys
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exeception import NetworksecurityException

load_dotenv()
MANG_DB_URL=os.getenv('MANG_DB_URL')
ca=certifi.where()

class NetworkSecurityExtract():
    def __init__(self,database,collection):
        try:
            self.dtatbase=database
            self.collection=collection
        except Exception as e:
            NetworksecurityException(e,sys)

    def csv_to_json_conveter(self,file_path):
        df=pd.read_csv(file_path)
        df.reset_index(drop=True,inplace=True)
        records=df.to_dict(orient="records")#this will transpose and give the list of dict
        return records
    
    def push_data_mango_db(self,records):
        self.records=records
        self.mango_client=pymongo.MongoClient(MANG_DB_URL)