from typing import TypeVar, Generic, Type

from pydantic import BaseModel

from src.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)



class CRUDBase(Generic[ModelType, CreateSchemaType]):
    """Base methods for models"""

    def __init__(self, model: Type[ModelType]):
        self.model = model
