import os
import sys

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier,RandomForestClassifier,GradientBoostingClassifier

from networksecurity.entiy.artifact_entity import DataTransformationArtifact
from networksecurity.entiy.config_entity import ModelTrainingConfig
from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.modeltraing_utility.modeltraing_utils import examine_the_model
from networksecurity.utils.main_utils.main import load_numpy_array,load_pickle_object,save_object
from networksecurity.utils.ml_utils.metrics_utils.classification_metrics import get_classification_report
from networksecurity.utils.ml_utils.modeltraing_utility.modeltraing_utils import examine_the_model
from networksecurity.utils.ml_utils.modeltraing_utility.networ_model import Networkmodel
from networksecurity.entiy.artifact_entity import ModeltrainingArtifact
from networksecurity.constant.trainingpipline import FINAL_MODEL_DIR,MODEL_FILE_NAME,PREPROCESSOR_FILE_NAME
import  mlflow
import dagshub
from dotenv import load_dotenv

load_dotenv()

tocken=os.getenv("DAGSHUB_TOKEN")
if tocken:
    dagshub.auth.add_app_token("")

# Initialize DagsHub
print("DAGSHUB_TOKEN:", os.getenv("DAGSHUB_TOKEN"))
dagshub.init(
    repo_owner="jaivenkateshofficial-lgtm",
    repo_name="cybersecurity",
    mlflow=True
)



class ModelTrainer:

    def __init__(self,data_tranformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainingConfig):
        try:
            self.data_tranformation_atrifact=data_tranformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            NetworksecurityException(e,sys)

    def track_ml_flow(self,model,classificationreport):
        with mlflow.start_run():
            fl_score=classificationreport.fl_score
            recall=classificationreport.recall
            precision=classificationreport.precision
            mlflow.log_metric('fl_score',fl_score)
            mlflow.log_metric('recall',recall)
            mlflow.log_metric('precision',precision)
            mlflow.sklearn.log_model(model)
    def model_traing(self,x_train,x_test,y_train,y_test):
        logging.info("started the model traing")
        models={
            "DecisionTreeClassifier":DecisionTreeClassifier(),
            "LogisticRegression":LogisticRegression(),
            "RandomForestClassifier":RandomForestClassifier(),
            "AdaBoostClassifier":AdaBoostClassifier(),
            "GradientBoostingClassifier":GradientBoostingClassifier()
        }

        params={
            "DecisionTreeClassifier":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                'max_depth':[10,12,13,5]
            },
             "LogisticRegression": {
                # 'solver': ['liblinear', 'saga'],
                # 'penalty': ['l1', 'l2'],
                'C': [0.1, 1.0, 10.0]
            },
            "RandomForestClassifier":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            
            "AdaBoostClassifier":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            },
            "GradientBoostingClassifier":{
                # 'learning_rate':[.1,.01,.05,.001],
                # 'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                'max_features':['sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            }
        }
        logging.info("starting the model selection")
        report:dict=examine_the_model(x_test=x_test,x_train=x_train,y_test=y_test,y_train=y_train,params=params,models=models)
        best_model_score = max(sorted(report.values()))
        best_model_name = list(report.keys())[
            list(report.values()).index(best_model_score)
        ]
        preprocessor=load_pickle_object(self.data_tranformation_atrifact.data_tranformation_object_file_path)
        best_model=Networkmodel(preprocessor=preprocessor,model=models[best_model_name])
        y_train_pred=best_model.predict_values(x_train)
        y_test_pred=best_model.predict_values(x_test)
        save_object(self.model_trainer_config.model_trained_file_path, best_model)
        classification_train_data_report=get_classification_report(y_true=y_train,y_pred=y_train_pred)
        classification_test_data_report=get_classification_report(y_true=y_test,y_pred=y_test_pred)
        self.track_ml_flow(best_model,classification_test_data_report)

        model_trained_artifact=ModeltrainingArtifact(trained_model_file_path=self.model_trainer_config.model_trained_file_path,train_metric_artifact=classification_train_data_report,test_metric_artifact=classification_test_data_report)
        model_file_path=os.path.join(FINAL_MODEL_DIR,MODEL_FILE_NAME)
        save_object(model_file_path,best_model)
        logging.info(f"model trained artifact:{model_trained_artifact}")
        return model_trained_artifact

    def intialize_model_traing(self):

        logging.info("model training has started")
        train:np.array=load_numpy_array(self.data_tranformation_atrifact.data_tranformation_train_file_path)
        test:np.array=load_numpy_array(self.data_tranformation_atrifact.data_tranformation_test_file_path)
        x_train=train[:,:-1]
        x_test=test[:,:-1]
        y_train=train[:,-1]
        y_test=test[:,-1]
        model_trained_artifact=self.model_traing(x_test=x_test,x_train=x_train,y_test=y_test,y_train=y_train)
        return model_trained_artifact
       
        
        

