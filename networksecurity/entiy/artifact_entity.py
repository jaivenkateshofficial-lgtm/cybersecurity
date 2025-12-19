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

@dataclass
class DataTransformationArtifact:
    data_tranformation_test_file_path:str
    data_tranformation_train_file_path:str
    data_tranformation_object_file_path:str

@dataclass
class Classificationreport:
    fl_score:int
    precision:int
    recall:int

@dataclass
class ModeltrainingArtifact:
    trained_model_file_path:str
    train_metric_artifact:str
    test_metric_artifact:str
