from fastapi import FastAPI
from pydantic import BaseModel
import src.services.ehentai as ehentai

app = FastAPI()

class Data(BaseModel):
    url: str
    user: str
    api_key: str



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/e-hentai")
async def e_hentai(data: Data):
    # check if the url is valid
    if not data.url.startswith('https://e-hentai.org/g/'):
        return {"message": "Invalid url"}

    # check if the user and api_key are valid
    if data.user != 'user' or data.api_key != 'api_key':
        return {"message": "Invalid user or api_key"}

    response = ehentai.main(data.url)
    if response == "Success":
        return {"message": "Success"}
    else:
        return {"message": "Error"}
