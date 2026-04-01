"""dummy fastapi (async) server. 

install dependencies:
$ pip install fastapi uvicorn
start server with:
$ uvicorn server_fastapi:app --reload --host 127.0.0.1 --port 8000 --workers 1

send requests to http://127.0.0.1:8000/
"""
from asyncio import sleep
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def status():
    await sleep(3)  # here can be async call to database to obtain status 
    return {"status": "io ok"}
