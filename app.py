import os
import sys

import certifi
ca=certifi.where()

from dotenv import load_dotenv
import fastapi
import pymongo
from networksecurity.pipline.training_pipline import Trainingpipline
from networksecurity.logging.logger import logging
from networksecurity.exception.exeception import NetworksecurityException

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,Request,UploadFile
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.responses import RedirectResponse
import pandas as pd
from fastapi.templating import Jinja2Templates
from networksecurity.constant.trainingpipline import DATA_INGESTION_COLLECTIONS
from networksecurity.constant.trainingpipline import DATA_INGESTION_DATA_BASE
from networksecurity.utils.main_utils.main import load_pickle_object
from networksecurity.entiy.config_entity import TrainingPippeLineConfig
from networksecurity.utils.ml_utils.modeltraing_utility.networ_model import Networkmodel
templates = Jinja2Templates(directory="./templates")

load_dotenv()
mongo_client=pymongo.MongoClient(os.getenv("MONGO_DB_URL"),tlsCAFile=ca)
database=mongo_client[DATA_INGESTION_DATA_BASE]
collection=database[DATA_INGESTION_COLLECTIONS]

mango_db_url=os.getenv("MONGO_DB_URL")

app=FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipline_config=TrainingPippeLineConfig()
        train_pipline=Trainingpipline(training_pipline_config=training_pipline_config)
        train_pipline.strat_pipeline()
        return Response("Training is done")
    except Exception as e:
        raise NetworksecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
        df.drop(columns='Result',inplace=True)
        preprocessor = load_pickle_object(os.path.join("final_model", "preprocesser.pkl"))
        loaded_model = load_pickle_object(os.path.join("final_model", "model.pkl"))

        # `loaded_model` may already be a wrapped Networkmodel (saved earlier)
        if hasattr(loaded_model, "predict_values"):
            model_wrapper = loaded_model
        else:
            model_wrapper = Networkmodel(preprocessor=preprocessor, model=loaded_model)

        y_predict = model_wrapper.predict_values(df)
        print(y_predict)
        df['predicted_column'] = y_predict
        print(f"the pridicted colums{df['predicted_column']}")
        os.makedirs('prediction_output',exist_ok=True)
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        raise NetworksecurityException(e,sys)
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
