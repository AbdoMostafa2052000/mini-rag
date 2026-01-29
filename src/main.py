from fastapi import FastAPI
from routes import base ## my .py file
from dotenv import load_dotenv ## loads .env to my os

load_dotenv(".env")
app = FastAPI()
app.include_router(base.base_router)







#“When a client requests this URL with this HTTP method, which code should run?”
#Uvcorn is responsble for runing FastAPI as web

# uvicorn main:app
#uvicorn main:app --reload --host 0.0.0.0 --port 5000
