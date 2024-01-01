from fastapi import FastAPI

from src.db.session import get_or_create_engine, dispose_engine
from src.api.users import router as users_router

app = FastAPI()
app.include_router(users_router, prefix="/api/users", tags=["Users"])


@app.on_event("startup")
async def startup():
    """Starts engine and logging on apps run"""
    get_or_create_engine()


@app.on_event("shutdown")
async def shutdown():
    """Stops engine on apps stop"""
    await dispose_engine()