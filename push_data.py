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

class NetworkSecurityDataExtract():
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
        try: 
            self.records=records
            self.mango_client=pymongo.MongoClient(MANG_DB_URL)
            self.dtatbase=self.mango_client[self.dtatbase]
            self.collection=self.dtatbase[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            NetworksecurityException(e,sys)

# if __name__=='__main__':
#     FILE_PATH="Network_Data\phisingData.csv"
#     DATABASE="Jai_db"
#     Collection="NetworkData"
#     networkobj=NetworkSecurityDataExtract(DATABASE,Collection)
#     records=networkobj.csv_to_json_conveter(file_path=FILE_PATH)
#     print(records)
#     no_of_records=networkobj.push_data_mango_db(records)
#     print(no_of_records)

