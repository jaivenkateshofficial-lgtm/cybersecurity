import os
import sys
import pandas as pd
import numpy as np

'''
Comman constant variables
'''
PIPELINE_NAME="Networksecurity"
TRAIN_DATA:str="train.csv"
TEST_DATA:str="test.csv"
RAW_DATA:str="raw.csv"
ARTICFACT_DIR_NAME:str="Artifact"
DATA_FILE:str="phisingData.csv"
PREDICTION_COLUM:str="Result"
RANDOM_STATE:int=10
DATA_SHEMA:str=os.path.join("Data_schema","schema.yaml")
VALID_TRAIN_DATA:str="valid_train.csv"
VALID_TEST_DATA:str="valid_test.csv"
INVALID_TRAIN_DATA:str="Invalid_train.csv"
INVALID_TEST_DATA:str="Invalid_test.csv"
DATA_VALIDATION_THRESHOLD:float=0.05

'''
Data ingestion related conctants
'''
DATA_INGESTION_DATA_BASE:str="Jai_db"
DATA_INGESTION_COLLECTIONS:str="NetworkData"
DATA_INGESTION_FEATURE_STORE:str="FeatureStore"
DATA_INGESTION_DIR_NAME:str="DataIngestion"
DATA_INGESTION_INGESTED_DIR:str="Ingested"
DATA_INGESTION_TRAIN_TEST_RATIO:float=0.2

'''
Data validation related contants
'''
DATA_VALIDATION_DIR:str="DataValidation"
DATA_VALIDATION_VALID_DATA="valid"
DATA_VALIDATION_INVALID_DATA="Invalid"
DATA_VALIDATION_REPORT="Report"



