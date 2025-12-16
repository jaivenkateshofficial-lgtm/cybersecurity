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

class ModelTrainer:

    def __init__(self,data_tranformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainingConfig):
        try:
            self.data_tranformation_atrifact=data_tranformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            NetworksecurityException(e,sys)

    def model_traing(self):
        logging.info("started the model traing")
        models={
            "DecisionTreeClassifier":DecisionTreeClassifier,
            "LogisticRegression":LogisticRegression,
            "RandomForestClassifier":RandomForestClassifier,
            "AdaBoostClassifier":AdaBoostClassifier,
            "GradientBoostingClassifier":GradientBoostingClassifier
        }

        params={
            "DecisionTreeClassifier":{
                'criterion':{'gini', 'entropy', 'log_loss'},
                'max_depth':{10,12,13,5}
            },
            "Logistic Regression":{
                'penalty':{'l1', 'l2', 'elasticnet', None},
                'solver':{'lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga'}
            },
            "Random Forest":{
                'criterion':['gini', 'entropy', 'log_loss'],
                'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            }
        }
        

