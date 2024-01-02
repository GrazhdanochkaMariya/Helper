from pydantic import BaseModel


class AdminSchemaCreate(BaseModel):
    """Schema for creating admin"""

    username: str
    password: str