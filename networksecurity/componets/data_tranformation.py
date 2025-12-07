import os
import sys

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.entiy.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entiy.config_entity import DataTranformationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.constant.trainingpipline import PREDICTION_COLUM

class DataTransformation:

    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            NetworksecurityException(e,sys)    

    @staticmethod
    def read_csv(file_path:str)->pd.DataFrame:
        try:
            pd.read_csv(file_path)
        except Exception as e:
            NetworksecurityException(e,sys)


    def intialise_data_transformation(self):
        logging.info('Data transformation has started')
        train_file_path=self.data_validation_artifact.valid_train_file_path
        test_file_path=self.data_validation_artifact.valid_test_file_path
        train_df=DataTransformation.read_csv(train_file_path)
        test_df=DataTransformation.read_csv(test_file_path)
        input_features_train=train_df.drop(columns=[PREDICTION_COLUM])
        output_features_train=train_df[PREDICTION_COLUM]
        input_features_test=test_df.drop(columns=[PREDICTION_COLUM])
        output_features_test=test_df([PREDICTION_COLUM])


