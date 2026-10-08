
from datetime import datetime, timezone
from polyglot.common.pagination import Page, Pagination
from sqlmodel import Session, select
from uuid import UUID

from polyglot.comments.schemas import CommentRead, CommentUpdate

from polyglot.comments.models import Comment

from polyglot.issues.service import get_issue

def get_comments(session: Session, issue_id: UUID, limit: int, cursor: UUID | None = None) -> Page[CommentRead] | None:
    issue = get_issue(session, issue_id)
    if not issue:
        return None

    stmt = (
        select(Comment)
        .where(Comment.issue_id == issue_id)
        .order_by(Comment.id)  # type: ignore
    )

    if cursor:
        stmt = stmt.where(Comment.id > cursor)

    response = session.exec(stmt.limit(limit)).all()

    return Page(
        items=[CommentRead.model_validate(comment) for comment in response],
        pagination=Pagination(limit=limit, next_cursor=str(response[-1].id) if len(response) == limit else None),
    )

def create_comment(session: Session, issue_id: UUID, body: str) -> Comment | None:
    issue = get_issue(session, issue_id)
    if not issue:
        return None
    
    comment = Comment.model_validate({"issue_id": issue_id, "body": body, "author_id": UUID(int=0)})  # Placeholder for author_id, replace with actual user ID
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

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