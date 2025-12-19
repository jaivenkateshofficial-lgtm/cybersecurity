import os
import sys

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from networksecurity.entiy.artifact_entity import DataTransformationArtifact
from networksecurity.entiy.config_entity import ModelTrainingConfig
from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.main import *

class Networkmodel:
    def  __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            NetworksecurityException(e,sys)

    def predict_values(self,x):
        try:
            preprocessor=self.preprocessor
            model=self.model
            x_transformed=preprocessor.transform(x)
            y_pred=model.predict(x_transformed)
            return y_pred
        except Exception as e:
            raise NetworksecurityException(e,sys)
