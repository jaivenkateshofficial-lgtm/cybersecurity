import os
import yaml
import sys

import numpy as np
import pandas as pd
import pickle
from networksecurity.exception.exeception import NetworksecurityException

def load_yaml(file_path:str)->dict:
    '''
    purpose:load the yaml file from specific path and give dict

    Args:
    file_path: Need to give the input file path

    Return:dictionary
    return the dictionary of all element in yaml file
    '''
    try:
        with open(file_path,'r') as file_obj:
            data_dict=yaml.safe_load(file_obj)

        return data_dict
    except Exception as e:
        raise NetworksecurityException(e,sys)
    
def write_yaml(directory,filename,content):
    try:
        file_path=os.path.join(directory,filename)
        with open(file_path,'w') as file_obj:
            yaml.dump(content,file_obj)
    except Exception as e:
        NetworksecurityException(e,sys)

def save_numpy_array(file_path,array)->None:
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as file_object:
            np.save(file_object,array)
    except Exception as e:
        NetworksecurityException(e,sys)

def save_object(file_path,object):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as file_object:
            pickle.dump(object,file_object)
    except Exception as e:
        NetworksecurityException(e,sys)

def load_pickle_object(file_path:str):
    try:
        if not (os.path.exists(file_path)):
            raise Exception
        with open(file_path) as file_obj:
            pickle.load(file_obj)
    except Exception as e:
        NetworksecurityException(e,sys)

def load_numpy_array(file_path:str)->np.array:
    try:
        if not (os.path.exists(file_path)):
            raise Exception
        with open(file_path) as file_obj:
            array=np.load(file_obj)
        return array
    except Exception as e:
        NetworksecurityException(e,sys)