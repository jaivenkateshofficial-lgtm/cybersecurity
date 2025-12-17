import os
import sys

import numpy
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score,recall_score,precision_score


def get_model_selction_report(models:dict,params,x_train,y_train,x_test,y_test)->dict:
    report={}
    for i in range(len(list(models))):
        model:DecisionTreeClassifier=list(models.values)[i]
        model_name=list(models.keys())[i]
        param=params[i]
        grid_cv=GridSearchCV(estimator=model,param_grid=param,cv=3)
        grid_cv.fit(x_train)
        best_params=grid_cv.best_params_
        model(**best_params)
        model.fit(x_train,y_train)
        y_train_pred=model.predict(x_train)
        y_test_pred=model.predict(x_test)
        f1=f1_score(y_true=y_test,y_pred=y_test_pred)
        recall=recall_score(y_true=y_test,y_pred=y_test_pred)
        precision=precision_score(y_true=y_test,y_pred=y_test_pred)
        report[model_name]={
            'fl_score':f1,
            'recall_score':recall,
            'precision_score':precision
        }

        return report



