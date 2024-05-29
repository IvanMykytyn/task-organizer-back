from fastapi import APIRouter, HTTPException
from app import crud

from app.api.deps import CurrentUser, SessionDep

router = APIRouter()


@router.post("/")
def add_source(session: SessionDep, current_user: CurrentUser, source_data: dict):
    try:
        source = crud.create_source(session=session, source_data={"user_id": current_user.id, **source_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return source

@router.get("/all")
def get_all_sources(session: SessionDep, current_user: CurrentUser):
    try:
        sources = crud.get_user_sources(session=session, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return sources

@router.post("/{source_id}/activate")
def activate_source(source_id: str, session: SessionDep, current_user: CurrentUser):
    try:
        source = crud.create_source(session=session, source_data={
            "is_active": True,
            "type": source_id,
            "user_id": current_user.id
        }
    )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return source

