from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import field_validator
from sqlmodel import SQLModel

from polyglot.common.validators import SafeText


class ProjectRead(SQLModel):
    id: UUID
    name: str
    key: str
    description: str | None = None
    status: Literal["active", "archived"]
    created_at: datetime
    updated_at: datetime
    
class ProjectCreate(SQLModel):
    name: SafeText
    key: SafeText
    description: SafeText | None = None


class ProjectUpdate(SQLModel):
    name: SafeText | None = None
    description: SafeText | None = None
    status: Literal["active", "archived"] | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str | None) -> str:

        if name is None:
            raise ValueError("Name cannot be None")
        return name