from pydantic import BaseModel, ConfigDict, field_validator
from itertools import count

class Post(BaseModel):
    id: int
    topic: str
    body: str

    @field_validator("topic", "body")
    @classmethod
    def validate_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip()

class UpdatePost(BaseModel):
    topic: str
    body: str

    @field_validator("topic", "body")
    @classmethod
    def valide_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Value must be not empty")

        return value.strip()

class PatchPost(BaseModel):
    topic: str | None = None
    body: str | None = None
    # тип тут определяется как str или None, при этом None добавляется если значение не передано

    @field_validator("topic", "body")
    @classmethod
    def valide_not_empty(cls, value):
        if value is None or not value.strip():
            raise ValueError("Field cannot be empty")
    
        return value.strip()

class CreatePost(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    topic: str
    body: str

    @field_validator("topic", "body")
    @classmethod
    def validate_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip()