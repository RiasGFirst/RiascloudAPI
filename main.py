from fastapi import FastAPI

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/e-hentai")
async def e_hentai():
    return {"message": "E-Hentai API"}
