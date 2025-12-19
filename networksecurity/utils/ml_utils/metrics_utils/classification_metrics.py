import os
import sys

import numpy as np
import pandas as pd

from networksecurity.exception.exeception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.entiy.artifact_entity import Classificationreport
from sklearn.metrics import f1_score,recall_score,precision_score


def get_classification_report(y_true,y_pred)->Classificationreport:
    try:
        f1=f1_score(y_true=y_true,y_pred=y_pred)
        recall=recall_score(y_true=y_true,y_pred=y_pred)
        precision=precision_score(y_true=y_true,y_pred=y_pred)
        clasification_metric_artifact=Classificationreport(fl_score=f1,recall=recall,precision=precision)

        return clasification_metric_artifact
    except Exception as e:
        raise NetworksecurityException(e,sys)