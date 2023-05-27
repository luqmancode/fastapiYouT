# sql alchemy create database table and query in python format orm translate to raw sql query.
# It needs database.py and models.py in app folder

from fastapi import FastAPI
from . import models
from . database import engine
from .routers import users, posts, auth, votes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def add_routers(app):
    app.include_router(users.router)
    app.include_router(posts.router)
    app.include_router(auth.router)
    app.include_router(votes.router)

add_routers(app)

# DDL to ORM
models.Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    return {"message": "Hello World"}





