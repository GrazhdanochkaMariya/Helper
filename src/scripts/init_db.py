import logging

from sqlalchemy import insert, select

from src.auth.auth import get_password_hash
from src.config import settings
from src.database import sync_session_maker
from src.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating initial data")
    if sync_session_maker:
        with sync_session_maker() as db:
            if settings.FIRST_SUPERUSER:
                query = select(User).filter_by(email=settings.FIRST_SUPERUSER)
                user = db.execute(query).scalar_one_or_none()
                if not user:
                    hashed_password = get_password_hash(
                        settings.FIRST_SUPERUSER_PASSWORD
                    )
                    query = (
                        insert(User)
                        .values(
                            {
                                "email": settings.FIRST_SUPERUSER,
                                "hashed_password": hashed_password,
                            }
                        )
                        .returning(User)
                    )
                    db.execute(query)
                    db.commit()
                    logger.info("Initial data created")
                    exit(0)
    else:
        raise Exception("Unable to initialize DB!")
    logger.info("Initialization skipped")


if __name__ == "__main__":
    main()
