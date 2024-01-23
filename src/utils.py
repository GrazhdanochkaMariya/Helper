from fastapi import status
from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Schema for message response"""

    message: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"message": "Some response"},
            ],
        },
    }


responses = {
    status.HTTP_200_OK: {"model": MessageResponse},
    status.HTTP_400_BAD_REQUEST: {"model": MessageResponse},
    status.HTTP_401_UNAUTHORIZED: {"model": MessageResponse},
    status.HTTP_404_NOT_FOUND: {"model": MessageResponse},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": MessageResponse},
}

CONTACT_NOT_FOUND_MESSAGE = "Contact not found"
