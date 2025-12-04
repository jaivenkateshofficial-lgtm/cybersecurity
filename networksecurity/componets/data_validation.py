# Genral imports
import os 
import sys
from dotenv import load_dotenv

# Data amniplation imports
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

# project specific imports
from networksecurity.logging.logger import logging
from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.entiy.config_entity import DataValidationConfig
from networksecurity.entiy.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.utils.main_utils.main import load_yaml



class Datavalidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_schema_config=load_yaml(self.data_validation_config.data_validation_schema)
        except Exception as e:
            raise NetworksecurityException(e,sys)

    @staticmethod
    def read_csv(file_path):
        try:
            df=pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def validate_number_of_colums(self,data_frame:pd.DataFrame):
        no_of_columns_actual=len(self.data_schema_config['columns'])
        no_of_columns_df=len(data_frame.columns.to_list())
        column_mismath_ststus=False
        if no_of_columns_actual!=no_of_columns_df:
            column_mismath_ststus=True
        return column_mismath_ststus
    def validate_numerical_columns(self,data_frame:pd.DataFrame):
        no_of_num_column_actual=len(self.data_schema_config['numerical_columns'])
        no_of_columns_df=len(data_frame.columns.to_list())
        column_mismath_ststus=False
        if no_of_num_column_actual!=no_of_columns_df:
            column_mismath_ststus=True
        return column_mismath_ststus
    
    def validate_data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame):
        distance1=base_df
        distance2=current_df
        is_data_drifted=False
        distance_between_data_points=ks_2samp(distance1,distance2)
        threshold=self.data_validation_config.distance_threshold
        if threshold<distance_between_data_points:
            is_data_drifted=True
        return is_data_drifted

    def Intilaize_data_validation(self):
        train_file_path=self.data_ingestion_artifact.trained_file_path
        test_file_path=self.data_ingestion_artifact.test_file_path
        drift_report_file_path=self.data_validation_config.data_validation_report
        train_df=Datavalidation.read_csv(train_file_path)
        test_df=Datavalidation.read_csv(test_file_path)
        status=self.validate_number_of_colums(train_df)
        if status:
            logging.info("The train data and the test data are mistmatched")
        else:
            status=self.validate_numerical_columns(train_df)
            if status:
                logging.info("The numerical columns are mismathching")
            else:

                status=self.validate_data_drift(train_df,test_df)
                if status:
                    logging.info("The data frame is drifted from train data")
                else:
                    valid_train_file_path=self.data_validation_config.train_data_valid_file_path
                    valid_test_file_path=self.data_validation_config.test_data_valid_file_path
                    os.makedirs(self.data_validation_config.data_validation_valid)
                    train_df.to_csv(valid_train_file_path)
                    test_df.to_csv(valid_test_file_path)

                    data_validation_artifact=DataValidationArtifact(
                        validation_satus=status,
                        valid_train_file_path=valid_train_file_path,
                        valid_test_file_path=valid_test_file_path,
                        Invalid_test_file_path=None,
                        Invalid_train_file_path=None,
                        data_report_path=drift_report_file_path
                    )
                    return data_validation_artifact
                
        Invalid_train_file_path=self.data_validation_config.train_data_valid_file_path
        InvaLid_test_file_path=self.data_validation_config.test_data_valid_file_path
        os.makedirs(self.data_validation_config.data_validation_valid)
        train_df.to_csv(valid_train_file_path)
        test_df.to_csv(valid_test_file_path)
        data_validation_artifact=DataValidationArtifact(
                        validation_satus=status,
                        valid_train_file_path=None,
                        valid_test_file_path=None,
                        Invalid_test_file_path=InvaLid_test_file_path,
                        Invalid_train_file_path=Invalid_train_file_path,
                        data_report_path= drift_report_file_path
                    )



