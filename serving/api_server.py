import model_server  # Pulls in the rpc services automatically

from fastapi import FastAPI    # as before
from pydantic import BaseModel # as before

app = FastAPI()

@app.get("/")
async def root():
    print('Hello World')
    return {"message": "Bellow World"}

class Article(BaseModel):
    txt: str

@app.post("/detect")
async def detect(data:Article):
    print(f'I rcved: {data.txt}')
    print('Detect')
    res = await model_server.MyModel().myfunction1.call( (data.txt, ) )
    return res

# uvicorn api_server:app --reload
# In browser : http://127.0.0.1:8000/docs