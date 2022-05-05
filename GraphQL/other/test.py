import uvicorn
from multiprocessing import Process

servers = {}
_api_process = None


from fastapi import FastAPI

app = FastAPI()

@app.get("/api")
def get_root():
    return {"Hello": "World"}

uvicorn.run(app, port=9992, host='0.0.0.0', root_path='')