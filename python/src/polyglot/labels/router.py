from fastapi import APIRouter, HTTPException, Query

from polyglot.common.pagination import Page
from polyglot.db.db import SessionDep
from polyglot.labels import service
from polyglot.labels.schemas import LabelCreate, LabelRead
from uuid import UUID

from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/labels", tags=["labels"])

@router.get("", response_model=Page[LabelRead])
def get_labels(session: SessionDep, limit: int = Query(20, ge=1, le=100), cursor: UUID | None = None):
    return service.list_labels(session, limit, cursor)

@router.post("", status_code=201, response_model=LabelRead)
def create_label(session: SessionDep, data: LabelCreate):
    try: 
      return service.create_label(session, data)
    except IntegrityError:
      raise HTTPException(status_code=422, detail=f"A label with the name of {data.name} already exists")

@router.delete("/{label_id}", status_code=204)
def delete_label(label_id: UUID, session: SessionDep):
    response =  service.delete_label(session, label_id)
    if not response:
        raise HTTPException(status_code=404, detail="Label not found")
    