import os
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import r2_score
import time
from networksecurity.logging.logger import logging, console_logger


def examine_the_model(models:dict,params,x_train,y_train,x_test,y_test)->dict:
    report={}
    for i in range(len(list(models))):
        model=list(models.values())[i]
        model_name=list(models.keys())[i]
        param=params[model_name]
        grid_cv=GridSearchCV(estimator=model,param_grid=param,cv=3)
        # timing GridSearch
        gs_start = time.time()
        grid_cv.fit(x_train,y_train)
        gs_elapsed = time.time() - gs_start
        console_logger.info(f"GridSearch finished for {model_name} in {gs_elapsed:.1f}s")

        best_params=grid_cv.best_params_
        model.set_params(**best_params)
        # timing final fit
        fit_start = time.time()
        model.fit(x_train,y_train)
        fit_elapsed = time.time() - fit_start
        console_logger.info(f"Final fit finished for {model_name} in {fit_elapsed:.1f}s (total {gs_elapsed+fit_elapsed:.1f}s)")

        y_test_pred=model.predict(x_test)
        y_test = np.asarray(y_test, dtype=int)
        y_test_pred = np.asarray(y_test_pred, dtype=int)
        score=r2_score(y_true=y_test,y_pred=y_test_pred)
        report[model_name]=score

    return report



