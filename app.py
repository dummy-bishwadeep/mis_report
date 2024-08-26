import logging
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from scripts.config import Service


def start_fastapi_app():
    load_dotenv()
    app = FastAPI()
    logging.info(f"App Starting at {Service.HOST}:{Service.PORT}")
    uvicorn.run("main:app", host=Service.HOST, port=int(Service.PORT))


if __name__ == "__main__":
    start_fastapi_app()
