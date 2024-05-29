from typing import Any

from fastapi import HTTPException
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, InternalSource, TickTickSource, User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_source(*, session: Session, source_data: dict):
    if source_data['type'] == 'tick_tick':
        source = TickTickSource(**source_data)
    elif source_data['type'] == 'internal':
        source = InternalSource(**source_data)
    else:
        raise HTTPException(status_code=400, detail="Invalid source type")

    session.add(source)
    session.commit()
    session.refresh(source)
    return source


all_sources = ['internal', 'tick_tick']
 
def get_difference(list1, list2):
    return [item for item in list1 if item not in list2]

def get_source_tables(disabled_sources: list[str] = []):
    if not disabled_sources:
        return [TickTickSource, InternalSource]
    
    sources = []
    available_sources = get_difference(all_sources, disabled_sources)
    if 'tick_tick' in available_sources:
        sources.append(TickTickSource)
        
    if 'internal' in available_sources:
        sources.append(InternalSource)
    return sources


def get_user_sources(*, session: Session, user_id: int):
    sources = []
    for table in get_source_tables():
        query = select(table).where(table.user_id == user_id)
        result = session.exec(query).first()
        if result:
            sources.append(dict(result))
    
    return sources


def get_user_sources_with_filters(*, session: Session, user_id: int, disabled_sources: list[str]):
    sources = []
    for table in get_source_tables(disabled_sources=disabled_sources):
        query = select(table).where(table.user_id == user_id)
        result = session.exec(query).first()
        if result:
            sources.append(dict(result))
    
    return sources


def create_item(*, session: Session, item_in: ItemCreate, owner_id: int) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item



def get_items(*, session: Session, owner_id: int):
    statement = (
        select(Item)
        .where(Item.owner_id == owner_id)
    )
    return session.exec(statement).all()