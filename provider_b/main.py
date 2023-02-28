import time

from fastapi import FastAPI, Response
from fastapi.responses import FileResponse


app = FastAPI()


@app.post('/search')
async def search():
    time.sleep(30)
    return FileResponse('response_b.xml')
