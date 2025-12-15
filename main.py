import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exeception import NetworksecurityException
import os 
import sys
from dotenv import load_dotenv


import pandas as pd
import numpy as np
import pymongo
from sklearn.model_selection import train_test_split

from networksecurity.logging.logger import logging
from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.entiy.config_entity import Dataingestionconfig,TrainingPippeLineConfig
from networksecurity.componets.data_injestion import Dataingestion
from networksecurity.componets.data_validation import Datavalidation
from networksecurity.entiy.config_entity import DataValidationConfig


if __name__=='__main__':
    try:
        trainpipline=TrainingPippeLineConfig()
        data_ingestion_config=Dataingestionconfig(trainpipline)
        data_ingestion=Dataingestion(data_ingestion_config)
        df=data_ingestion.create_dataframe_from_database()
        status_feature=data_ingestion.save_data_in_feature_store(df)
        if status_feature:
            dtat_ingestion_artifact=data_ingestion.save_train_test_split(df)
            data_validation_config=DataValidationConfig(trainpipline)
            data_validation=Datavalidation(data_ingestion_artifact=dtat_ingestion_artifact,data_validation_config=data_validation_config)
            a=data_validation.Intilaize_data_validation()

            
    except Exception as e:
        raise NetworksecurityException(e,sys)