from di.init_dependencies import init_dependencies
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.messages import router as message_router


def create_app() -> FastAPI:
    app = FastAPI()
    init_dependencies(app)
    app.include_router(auth_router)
    app.include_router(message_router)
    return app


app = create_app()
