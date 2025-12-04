from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    validation_satus:bool
    valid_train_file_path:str
    valid_test_file_path:str
    Invalid_train_file_path:str
    Invalid_test_file_path:str
    data_report_path:str


