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


if __name__=='__main__':
    try:
        trainpipline=TrainingPippeLineConfig()
        a=Dataingestionconfig(trainpipline)
        di=Dataingestion(a)
        df=di.create_dataframe_from_database()
        status_feature=di.save_data_in_feature_store(df)
        if status_feature:
            artifact=di.save_train_test_split(df)
            print(artifact)
            
    except Exception as e:
        raise NetworksecurityException(e,sys)