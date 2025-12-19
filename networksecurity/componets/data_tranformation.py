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
from networksecurity.constant.trainingpipline import PREDICTION_COLUM,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.main import save_numpy_array,save_object

class DataTransformation:

    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTranformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            NetworksecurityException(e,sys)    

    @staticmethod
    def read_csv(file_path:str)->pd.DataFrame:
        try:
            df=pd.read_csv(file_path)
            return df
        except Exception as e:
            NetworksecurityException(e,sys)

    def get_data_transformation_object(self)->Pipeline:
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipline_object=Pipeline([("imputer",imputer)])
            return pipline_object
        except Exception as e:
            NetworksecurityException(e,sys)


    def intialise_data_transformation(self)->DataTransformationArtifact:
        logging.info('Data transformation has started')
        train_file_path=self.data_validation_artifact.valid_train_file_path
        test_file_path=self.data_validation_artifact.valid_test_file_path
        train_df=DataTransformation.read_csv(train_file_path)
        test_df=DataTransformation.read_csv(test_file_path)
        input_features_train:pd.DataFrame=train_df.drop(columns=[PREDICTION_COLUM])
        output_features_train:pd.DataFrame=train_df[PREDICTION_COLUM]
        input_features_test:pd.DataFrame=test_df.drop(columns=[PREDICTION_COLUM])
        output_features_test:pd.DataFrame=test_df[PREDICTION_COLUM]
        output_features_test:pd.DataFrame=output_features_test.replace(-1,0)
        output_features_train:pd.DataFrame=output_features_train.replace(-1,0)
        preprocessor=self.get_data_transformation_object()
        
        preprocessor_fitted=preprocessor.fit(input_features_train)
        input_features_train_transformed=preprocessor_fitted.transform(input_features_train)
        input_features_test_tranformed=preprocessor_fitted.transform(input_features_test)
        total_train_data=np.c_[input_features_train_transformed,np.array(output_features_train)]
        total_test_data=np.c_[input_features_test_tranformed,np.array(output_features_test)]
        save_object(file_path=self.data_transformation_config.data_transformation_object_file_path,object=preprocessor_fitted)
        save_numpy_array(self.data_transformation_config.data_transformation_train_file_path,total_train_data)
        save_numpy_array(self.data_transformation_config.data_transformation_test_file_path,total_test_data)
        data_transformation_artifact=DataTransformationArtifact(
            data_tranformation_object_file_path=self.data_transformation_config.data_transformation_object_file_path,
            data_tranformation_train_file_path=self.data_transformation_config.data_transformation_train_file_path,
            data_tranformation_test_file_path=self.data_transformation_config.data_transformation_test_file_path
                                                                )
        return data_transformation_artifact
        

