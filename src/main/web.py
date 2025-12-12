from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.main.config import config
from src.main.container import container
from src.presentation.fastapi.setup import setup_routes

app = FastAPI(title=config.api.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_routes(app, config)
setup_dishka(container, app)
