import io

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel 
from PIL import Image
import numpy as np

import model_server  # Pulls in the rpc services automatically


app = FastAPI()
model = model_server.MyModel()

@app.get("/")
async def root():
    print('Hello World')
    return {"message": "Bellow World"}

@app.post("/detect")
async def detect(data: UploadFile = File(...)):
    image = await data.read()
    image = np.array(Image.open(io.BytesIO(image)))

    res = await model.infer.call( image )
    return { "results": res }

# uvicorn api_server:app --reload
# In browser : http://127.0.0.1:8000/docs