from uuid import UUID
from polyglot.common.pagination import Pagination, Page
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from polyglot.labels.models import Label
from polyglot.labels.schemas import LabelRead, LabelCreate

def list_labels(session: Session, limit: int, cursor: UUID | None = None) -> Page[LabelRead]:
    stmt = select(Label).order_by(Label.id) # type: ignore
    if cursor:
        stmt = stmt.where(Label.id > cursor)
    response = session.exec(stmt.limit(limit)).all()
    return Page(items=[LabelRead.model_validate(label) for label in response], pagination=Pagination(limit=limit, next_cursor=str(response[-1].id) if len(response) == limit else None))

def get_label(session: Session, id: UUID) -> Label | None:
    return session.get(Label, id)

def create_label(session: Session, data: LabelCreate) -> Label:
    label = Label.model_validate(data)
    session.add(label)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise
    session.refresh(label)
    return label

def delete_label(session: Session, id: UUID) -> bool:
    label = get_label(session, id)
    if not label:
        return False
    session.delete(label)
    session.commit()
    return True