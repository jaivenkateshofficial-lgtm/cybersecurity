import os
import sys
from networksecurity.logging.logger import logging

class NetworksecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        _,_,error_tb=error_details.exc_info()
        self.file_name=error_tb.tb_frame.f_code.co_filename
        self.line_no=error_tb.tb_lineno
        self.error_message=error_message

    def __str__(self):
        return f"The error occured  on the file :{self.file_name} in the line number :{self.line_no} and error message is {self.error_message}"
    
