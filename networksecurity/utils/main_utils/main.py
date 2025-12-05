import os
import yaml
import sys

import numpy
import pandas as pd

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