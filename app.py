from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from routes.index_ruotes import home
from dotenv import load_dotenv
from fastapi import FastAPI
import os

load_dotenv()

middleware = [Middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])]

app = FastAPI(
    title="Send email app",
    description="Fastapi application to send email",
    version="1.0",
    middleware=middleware,
)

app.include_router(home)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
