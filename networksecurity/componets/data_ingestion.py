import os 
import sys
from dotenv import load_dotenv


import pandas as pd
import numpy as np
import pymongo
from sklearn.model_selection import train_test_split

from networksecurity.logging.logger import logging
from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.entiy.config_entity import Dataingestionconfig
from networksecurity.entiy.artifact_entity import DataIngestionArtifact
load_dotenv()

class Dataingestion:
    def  __init__(self,data_ingestion_config:Dataingestionconfig):
        try:
            self.data_ingestion_config=data_ingestion_config
            
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def create_dataframe_from_database(self):
        try:
            self.mongo_client=pymongo.MongoClient(os.getenv("MONGO_DB_URL"))
            data_base=self.data_ingestion_config.data_base_name
            collectiion=self.data_ingestion_config.data_collection
            df=pd.DataFrame(list(self.mongo_client[data_base][collectiion].find()))#the find will fetch the particular data
            if '_id' in df.columns.to_list():
                df.drop(columns='_id',inplace=True)
            df.replace('na',np.nan)
            return df
        except Exception as e:
            raise NetworksecurityException(e,sys)

    def save_data_in_feature_store(self,df:pd.DataFrame):
        try:
            feature_store=self.data_ingestion_config.feature_store
            feature_file=self.data_ingestion_config.feature_file_path
            os.makedirs(feature_store,exist_ok=True)
            df.to_csv(feature_file)
            logging.info("The features are stored")
            return True
        except Exception as e:
           raise NetworksecurityException(e,sys)
    
    def save_train_test_split(self,df:pd.DataFrame):
        try:
            logging.info("Train and test split started")
            output_feature_name=self.data_ingestion_config.output_feature_name
            randomstate=self.data_ingestion_config.random_state
            testsize=self.data_ingestion_config.train_test_split_ratio
            train,test=train_test_split(df,test_size=testsize,random_state=randomstate)
            train_df=pd.DataFrame(train)
            test_df=pd.DataFrame(test)
            trainfile=self.data_ingestion_config.train_data_file_path
            testfile=self.data_ingestion_config.test_data_file_path
            insgested=self.data_ingestion_config.data_ingested_store
            os.makedirs(insgested)
            train_df.to_csv(trainfile,index=False,header=True)
            test_df.to_csv(testfile,index=False,header=True)
            logging.info("Saved train and test split completed")
            data_ingestion_artifact=DataIngestionArtifact( trained_file_path=trainfile,test_file_path=testfile)
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworksecurityException(e,sys) 


