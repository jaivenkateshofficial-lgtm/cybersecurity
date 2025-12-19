import os
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import r2_score


def examine_the_model(models:dict,params,x_train,y_train,x_test,y_test)->dict:
    report={}
    for i in range(len(list(models))):
        model=list(models.values())[i]
        model_name=list(models.keys())[i]
        param=params[model_name]
        grid_cv=GridSearchCV(estimator=model,param_grid=param,cv=3)
        grid_cv.fit(x_train,y_train)
        best_params=grid_cv.best_params_
        model.set_params(**best_params)
        model.fit(x_train,y_train)
        y_test_pred=model.predict(x_test)
        y_test = np.asarray(y_test, dtype=int)
        y_test_pred = np.asarray(y_test_pred, dtype=int)
        score=r2_score(y_true=y_test,y_pred=y_test_pred)
        report[model_name]=score

    return report



