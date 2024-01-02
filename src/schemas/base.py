"""Module contains base schemas"""
from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Schema for message response"""

    message: str

    model_config = {"json_schema_extra": {"examples": [{"message": "Some response"}]}}
