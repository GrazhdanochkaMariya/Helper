from fastapi import FastAPI

from src.api.users import router as users_router
from src.api.auth import router as admin_auth


app = FastAPI()
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(admin_auth, prefix="/api/auth", tags=["Auth"])


