from fastapi import FastAPI
from .routers import notes

def create_app():
    app = FastAPI()
    app.include_router(notes.router)
    return app

app = create_app()
