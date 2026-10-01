
from datetime import datetime, timezone
from sqlmodel import Session
from uuid import UUID

from polyglot.comments.schemas import CommentUpdate

from polyglot.comments.models import Comment

def update_comment(session: Session, comment_id: UUID, data: CommentUpdate) -> Comment | None:
    comment = session.get(Comment, comment_id)
    if not comment:
        return None
    comment.body = data.body
    comment.updated_at = datetime.now(timezone.utc)

    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

def delete_comment(session: Session, comment_id: UUID) -> bool:
    comment = session.get(Comment, comment_id)
    if not comment:
        return False
    session.delete(comment)
    session.commit()
    return True