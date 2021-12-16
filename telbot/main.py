import uvicorn
from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from devtools import debug

from telbot import models

from telbot import api

app = FastAPI()


@app.on_event("startup")
def startup():
    from telbot.database import engine

    app.mount("/static", StaticFiles(directory="static"), name="static")
    models.Base.metadata.create_all(bind=engine)


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return "hello world"


app.include_router(api.router)


if __name__ == "__main__":
    uvicorn.run("telbot.main:app", reload=True)
