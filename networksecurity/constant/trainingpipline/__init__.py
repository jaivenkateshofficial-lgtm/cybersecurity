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
ARTICFACT__DIR_NAME:str="Artifact"
DATA_FILE:str="phisingData.csv"
PREDICTION_COLUM:str="Result"
RANDOM_STATE:int=10

'''
Data ingestion related conctants
'''
DATA_INGESTION_DATA_BASE:str="Jai_db"
DATA_INGESTION_COLLECTIONS:str="NetworkData"
DATA_INGESTION_FEATURE_STORE:str="FeatureStore"
DATA_INGESTION_DIR_NAME:str="DataIngestion"
DATA_INGESTION_INGESTED_DIR:str="Ingested"
DATA_INGESTION_TRAIN_TEST_RATIO:float=0.2


