from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from uuid import UUID

from polyglot.common.pagination import Pagination, Page
from polyglot.issues.errors import AssigneeNotFoundError, LabelNotFoundError
from polyglot.issues.models import Issue
from polyglot.issues.schemas import IssueCreate, IssueRead
from polyglot.labels.models import Label
from polyglot.users.models import User


def to_issue_read(issue: Issue) -> IssueRead:
    return IssueRead(
        id=issue.id,
        project_id=issue.project_id,
        title=issue.title,
        description=issue.description,
        status=issue.status,
        label_ids=[label.id for label in issue.labels],
        assignee_ids=[user.id for user in issue.assignees],
        created_at=issue.created_at,
        updated_at=issue.updated_at,
    )


def get_issues(session: Session, project_id: UUID, limit: int, cursor: UUID | None = None) -> Page[IssueRead]:
    stmt = (
        select(Issue)
        .where(Issue.project_id == project_id)
        .options(
            selectinload(Issue.labels),  # type: ignore
            selectinload(Issue.assignees),  # type: ignore
        )
        .order_by(Issue.id) # type: ignore
    )
    if cursor:
        stmt = stmt.where(Issue.id > cursor)
    response = session.exec(stmt.limit(limit)).all()
    return Page(
        items=[to_issue_read(issue) for issue in response],
        pagination=Pagination(limit=limit, next_cursor=str(response[-1].id) if len(response) == limit else None),
    )


def create_issue(session: Session, project_id: UUID, data: IssueCreate) -> IssueRead:
    labels = _fetch_by_ids(session, Label, data.label_ids)
    missing_labels = set(data.label_ids) - {label.id for label in labels}
    if missing_labels:
        raise LabelNotFoundError(f"Labels not found: {_join(missing_labels)}")

    users = _fetch_by_ids(session, User, data.assignee_ids)
    missing_users = set(data.assignee_ids) - {user.id for user in users}
    if missing_users:
        raise AssigneeNotFoundError(f"Assignees not found: {_join(missing_users)}")

    issue = Issue(project_id=project_id, title=data.title, description=data.description)
    issue.labels = labels
    issue.assignees = users

    session.add(issue)
    session.commit()
    session.refresh(issue)
    return to_issue_read(issue)

def _fetch_by_ids(session: Session, model, ids: list[UUID]) -> list:
    if not ids:
        return []
    return list(session.exec(select(model).where(model.id.in_(ids))).all())

def _join(ids: set[UUID]) -> str:
    return ", ".join(sorted(str(i) for i in ids))
