from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

class TaskType(Enum):
    TICK_TICK = "tick-tick"
    INTERNAL = "internal"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


class UserUpdate(UserBase):
    email: str | None = None
    password: str | None = None


class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str



class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
    
    
class ItemBase(SQLModel):
    title: str
    description: str | None = None
    color: str
    priority: str

class ItemCreate(ItemBase):
    title: str


class ItemUpdate(ItemBase):
    title: str | None = None


class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: int | None = None
    email: str


class NewPassword(SQLModel):
    token: str
    new_password: str


class SourceBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    is_active: bool = True
    type: str
    user_id: int = Field(default=None, foreign_key="user.id")
    

class TickTickSource(SourceBase, table=True):
    __tablename__ = "tick_tick_source"
    test: str | None

class InternalSource(SourceBase, table=True):
    __tablename__ = "internal_source"


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")

class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    color: str
    description: str
    priority: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")
