from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel
from app import crud

from app.clients.openai.client import OpenAIClient
from app.data.sources.source_factory import get_handler_class_by_source_id
from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate

router = APIRouter()


@router.get("/all")
def get_all_tasks(
    session: SessionDep, 
    current_user: CurrentUser,
) -> Any:
    sources = crud.get_user_sources(session=session, user_id=current_user.id)
    tasks = []
    
    for source in sources:
        handler_class = get_handler_class_by_source_id(source['type'])
        handler = handler_class(user_id=current_user.id, user_email=current_user.email)
        tasks.extend(handler.get_tasks(session))
    return tasks    


@router.get("")
def get_tasks(
    session: SessionDep, current_user: CurrentUser, disabled_sources: str = Query(None), q: str = Query(None)
) -> Any:
    disabled_sources = disabled_sources.split(',')
    sources = crud.get_user_sources_with_filters(session=session, user_id=current_user.id, disabled_sources=disabled_sources)
    tasks = []
    
    for source in sources:
        handler_class = get_handler_class_by_source_id(source['type'])
        handler = handler_class(user_id=current_user.id, user_email=current_user.email)
        tasks.extend(handler.get_tasks(session, q=q))
    return tasks    

 
@router.post("/manual")
def create_task_manual(
    session: SessionDep, 
    current_user: CurrentUser,
    item_in: ItemCreate
) -> Any:
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

 
 
class ItemCreateWithAI(BaseModel):
    prompt: str
 

@router.post("/ai-helper")
def create_task_with_ai_helper(
    session: SessionDep, 
    current_user: CurrentUser,
    item_in: ItemCreateWithAI
) -> Any:
    response = OpenAIClient.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant",
            },
            {
                "role": "user",
                "content": item_in.prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    # breakpoint()
    # item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    # session.add(item)
    # session.commit()
    # session.refresh(item)
    # return item

 