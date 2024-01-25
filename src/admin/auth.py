from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.auth import authenticate_user, create_access_token
from src.auth.dependencies import get_current_user
from src.config import settings
from src.database import async_session_maker


class SessionAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        async with async_session_maker() as session:
            user = await authenticate_user(email, password, session)
            if user:
                access_token = create_access_token({"sub": str(user.id)})
                request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        async with async_session_maker() as session:
            user = await get_current_user(token, session)
            if not user:
                return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = SessionAuth(secret_key=settings.SECRET_KEY)
