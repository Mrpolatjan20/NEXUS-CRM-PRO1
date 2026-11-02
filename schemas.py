from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str = Field(min_length=8)
    role: str = "OPERATOR"


class ClientCreate(BaseModel):
    full_name: str
    phone: str
    pinfl: str | None = None
    address: str | None = None


class ClientOut(BaseModel):
    id: int
    full_name: str
    phone: str
    pinfl: str | None
    address: str | None
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(BaseModel):
    client_id: int
    title: str
    description: str | None = None


class ApplicationDecision(BaseModel):
    status: str
    description: str | None = None


class ApplicationOut(BaseModel):
    id: int
    client_id: int
    title: str
    description: str | None
    status: str
    created_by: int
    decided_by: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationRead(BaseModel):
    is_read: bool = True


class KPIRecordCreate(BaseModel):
    user_id: int
    sales_count: int = Field(default=0, ge=0)
    sales_amount: int = Field(default=0, ge=0)
    collection_amount: int = Field(default=0, ge=0)
    period: str = Field(pattern=r"^\d{4}-\d{2}$")


class SyncItem(BaseModel):
    client_operation_id: str
    operation: str
    payload: dict[str, Any]


class SyncRequest(BaseModel):
    device_id: str
    items: list[SyncItem]


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)