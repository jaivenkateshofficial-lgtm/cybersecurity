from datetime import datetime
import os
import sys
import numpy as np
import pandas as pd
from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.constant import trainingpipline

class TrainingPippeLineConfig:
    def __init__(self,timestamp=datetime.now()):
        try:
            self.timestamp=datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
            self.pipline_name=trainingpipline.PIPELINE_NAME
            self.artifactname=trainingpipline.ARTICFACT_DIR_NAME
            self.artifact_dir=os.path.join(self.artifactname,self.timestamp)
        except Exception as e:
            NetworksecurityException(e,sys)

class Dataingestionconfig:
    def __init__ (self,training_pipeline_config:TrainingPippeLineConfig):
        self.data_ingestion_directory=os.path.join(training_pipeline_config.artifact_dir,trainingpipline.DATA_INGESTION_DIR_NAME)
        self.feature_store=os.path.join(self.data_ingestion_directory,trainingpipline.DATA_INGESTION_FEATURE_STORE)
        self.feature_file_path=os.path.join(self.feature_store,trainingpipline.RAW_DATA)
        self.data_ingested_store=os.path.join(self.data_ingestion_directory,trainingpipline.DATA_INGESTION_INGESTED_DIR)
        self.train_data_file_path=os.path.join(self.data_ingested_store,trainingpipline.TRAIN_DATA)
        self.test_data_file_path=os.path.join(self.data_ingested_store,trainingpipline.TEST_DATA)
        self.train_test_split_ratio=trainingpipline.DATA_INGESTION_TRAIN_TEST_RATIO
        self.data_base_name=trainingpipline.DATA_INGESTION_DATA_BASE
        self.data_collection=trainingpipline.DATA_INGESTION_COLLECTIONS
        self.output_feature_name=trainingpipline.PREDICTION_COLUM
        self.random_state=trainingpipline.RANDOM_STATE

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPippeLineConfig):
        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,trainingpipline.DATA_VALIDATION_DIR)
        self.data_validation_valid=os.path.join(self.data_validation_dir,trainingpipline.DATA_VALIDATION_VALID_DATA)
        self.data_validation_invalid=os.path.join(self.data_validation_dir,trainingpipline.DATA_VALIDATION_INVALID_DATA)
        self.train_data_valid_file_path=os.path.join(self.data_validation_valid,trainingpipline.VALID_TRAIN_DATA)
        self.test_data_valid_file_path=os.path.join(self.data_validation_valid,trainingpipline.VALID_TEST_DATA)
        self.train_data_invalid_file_path=os.path.join(self.data_validation_invalid,trainingpipline.INVALID_TRAIN_DATA)
        self.test_data_invalid_file_path=os.path.join(self.data_validation_invalid,trainingpipline.INVALID_TEST_DATA)
        self.data_validation_schema=trainingpipline.DATA_SHEMA
        self.distance_threshold=trainingpipline.DATA_VALIDATION_THRESHOLD
        self.data_validation_report=trainingpipline.DATA_VALIDATION_REPORT

class DataTranformationConfig:
    def __init__(self,training_pipeline_config:TrainingPippeLineConfig):
       self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,trainingpipline.DATA_TRANSFORMATION_DIR)
       self.data_transformation_train_file_path=os.path.join(self.data_transformation_dir,trainingpipline.DATA_TRANSFORMATION_TRAIN_FILE_NAME)
       self.data_transformation_test_file_path=os.path.join(self.data_transformation_dir,trainingpipline.DATA_TRANSFORMATION_TEST_FILE_NAME)
       self.data_transformation_object_file_path=os.path.join(self.data_transformation_dir,trainingpipline.DATA_TRANSFORMATION_OBJECT_FILE_NAME)

class ModelTrainingConfig:
    def __init__(self,training_pipeline_config:TrainingPippeLineConfig):
        self.model_training_dir=os.path.join(training_pipeline_config.artifact_dir,trainingpipline.MODEL_TRAINING_DIR)
        self.model_trained_file_path=os.path.join(self.model_training_dir,trainingpipline.BEST_MODEL_NAME)
        self.model_expected_threshold=trainingpipline.MODEL_BASE_THRESHOLD
        self.overfittting_underfitting_threshold=trainingpipline.MODEL_OVERFITTING_UNDERFITTING_THRESHOLD
