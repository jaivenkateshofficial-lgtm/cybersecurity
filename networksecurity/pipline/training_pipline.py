import os
import sys

from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant import trainingpipline
from networksecurity.entiy.config_entity import TrainingPippeLineConfig
from networksecurity.entiy.config_entity import(
    Dataingestionconfig,
    DataValidationConfig,
    DataTranformationConfig,
    ModelTrainingConfig
)
from networksecurity.entiy.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModeltrainingArtifact
)
from networksecurity.componets.data_tranformation import DataTransformation
from networksecurity.componets.data_ingestion import Dataingestion
from networksecurity.componets.data_validation import Datavalidation
from networksecurity.componets.model_trainer import ModelTrainer


class Trainingpipline:

    def __init__(self,training_pipline_config:TrainingPippeLineConfig):
        self.training_pipline_config=training_pipline_config

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("data ingestion has started")
            data_ingestion_config=Dataingestionconfig(training_pipeline_config=self.training_pipline_config)
            data_ingestion =Dataingestion(data_ingestion_config=data_ingestion_config)
            df=data_ingestion.create_dataframe_from_database()
            status_feature=data_ingestion.save_data_in_feature_store(df)
            if status_feature:
                data_ingestion_artifact=data_ingestion.save_train_test_split(df)
            logging.info(f'The data dataingestion is completed and the artifact is {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
           logging.info("data validation has started")
           data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipline_config)
           data_validation=Datavalidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
           data_validation_artifact=data_validation.Intilaize_data_validation()
           return data_validation_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact)->DataTransformationArtifact:
        try:
           logging.info("data tranformation has started")
           data_transformation_config=DataTranformationConfig(training_pipeline_config=self.training_pipline_config)
           data_transformation=DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
           data_transformation_artifact=data_transformation.intialise_data_transformation()
           logging.info(f'The data dataingestion is completed and the artifact is {data_validation_artifact}')
           return data_transformation_artifact
        
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact)->ModeltrainingArtifact:
        try:
           logging.info("model training has started")
           model_training_config=ModelTrainingConfig(training_pipeline_config=self.training_pipline_config)
           model_trainer=ModelTrainer(data_tranformation_artifact=data_transformation_artifact,model_trainer_config=model_training_config)
           model_trained_artifat=model_trainer.intialize_model_traing()
           logging.info(f"The model traing has completed and the model trained artifact is {model_trained_artifat}")
           return model_trained_artifat
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def strat_pipeline(self):
        try:
           logging.info("started the machine learnin pipline")
           
           data_ingestion_artifact= self.start_data_ingestion()
           data_validation_arifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
           data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_arifact)
           model_trainer_artifact=self.start_model_training(data_transformation_artifact=data_transformation_artifact)
           return model_trainer_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
        

if __name__=='__main__':
    training_pipline_config=TrainingPippeLineConfig()
    train_pipline=Trainingpipline(training_pipline_config=training_pipline_config)
    train_pipline.strat_pipeline()

