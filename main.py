from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app.api.events.routers import events_router
from app.api.bets.routers import bets_router

from app.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    application = FastAPI(version="1.0.0", middleware=middleware)

    application.add_event_handler(
        "startup",
        create_start_app_handler(),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(),
    )
    application.include_router(events_router)
    application.include_router(bets_router)

    return application


app = get_application()
