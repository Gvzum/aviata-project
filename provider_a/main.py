import time

from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI()


@app.post('/search')
async def search():
    time.sleep(10)
    return FileResponse('response_a.json')
