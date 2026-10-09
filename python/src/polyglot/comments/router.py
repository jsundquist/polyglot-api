from uuid import UUID

from fastapi import APIRouter, HTTPException

from polyglot.comments import service
from polyglot.comments.schemas import CommentRead, CommentUpdate
from polyglot.db.db import SessionDep

router = APIRouter(prefix="/comments", tags=["comments"])

@router.patch("/{comment_id}", response_model=CommentRead)
def update_comment(session: SessionDep, comment_id: UUID, data: CommentUpdate):
    comment = service.update_comment(session, comment_id, data)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment

@router.delete("/{comment_id}", status_code=204)
def delete_comment(session: SessionDep, comment_id: UUID):
    response = service.delete_comment(session, comment_id)
    if not response:
        raise HTTPException(status_code=404, detail="Comment not found")