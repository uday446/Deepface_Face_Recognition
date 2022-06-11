from flask import Flask, render_template,request
from utils.all_utils import read_yaml
from flask_cors import CORS, cross_origin
import webbrowser
from threading import Timer
import pandas as pd
import pickle
import logging
import os
import subprocess
import yaml
import argparse
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.encoders import jsonable_encoder

import clientApp
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'webapp.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


app = FastAPI() # initializing a flask app
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
    max_age=2
    )
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post('/login',response_class=HTMLResponse)
async def login(request:Request):
    try:
        form_data = await request.form()
        USER_NAME = form_data['USER_NAME']
        USER_PASSWORD = form_data['USER_PASSWORD']
        dict_file = {
            'USER_NAME': USER_NAME,
            'index_name' : 'face_recognition'
        }
        with open('config/config.yaml', 'w') as file:
            yaml.dump(dict_file, file)
        return templates.TemplateResponse("register.html", {"request": request})
    except Exception as e:
        logging.error(e)

@app.get('/login',response_class=HTMLResponse)
async def login(request:Request):
    try:
        return templates.TemplateResponse("register.html", {"request": request})
    except Exception as e:
        logging.error(e)


@app.get('/signup',response_class=HTMLResponse)
async def signup(request:Request):
    try:
        return templates.TemplateResponse("signup.html", {"request": request})
    except Exception as e:
        print("Inside Except")
        print(e)
        logging.error(e)


@app.post('/signup',response_class=HTMLResponse)
async def signup(request:Request):
    try:
        form_data = await request.form()
        print("Inside Try")
        USER_NAME = form_data['USER_NAME']
        print(USER_NAME)
        EMAIL_ID = form_data['EMAIL_ID']
        print(EMAIL_ID)
        USER_PASSWORD = form_data['USER_PASSWORD']
        dict_file = {
            'USER_NAME': USER_NAME,
            'index_name' : 'face_recognition'
        }
        with open('config/config.yaml', 'w') as file:
            yaml.dump(dict_file, file)
            file.close()
        generate = clientApp.getFaceEmbeddings()
        return templates.TemplateResponse("signup.html", {"request": request})
    except Exception as e:
        print("Inside Except")
        print(e)
        logging.error(e)


@app.get('/predict',response_class=HTMLResponse)
async def predict(request:Request):
    try:
        predict = clientApp.getFacePrediction()
        return templates.TemplateResponse("register.html", {"request": request})
    except Exception as e:
        # print("Inside Except")
        logging.error(e)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')


def start_app():
    Timer(3, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    start_app()

