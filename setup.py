from setuptools import find_packages,setup
from typing import List

def get_requirments()->List:
    '''
    This function will retun a list of requirmrnt from requirmrnt.txt file
    '''
    try:
        requiments_list=[]
        with open('requirement.txt','r') as file_obj:
            lines=file_obj.readlines()
            for line in lines:
                # ignoring emty spaces(it is not there but as good practice keeping)
                requiments=line.strip()
                # ignore the empty lines
                if requiments and requiments !='-e .':
                    requiments_list.append(requiments)
        return requiments_list
    except Exception as e:
        print(f'An exeception has occured {e}')

setup(

    name="networksecurity",
    version='0.0.1',
    author='Jai venkatesh',
    author_email='jaivenkateshofficial@gmail.com',
    packages=find_packages(),
    install_requires=get_requirments()
)