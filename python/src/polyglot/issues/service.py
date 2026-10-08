from datetime import datetime, timezone

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from uuid import UUID

from polyglot.common.pagination import Pagination, Page
from polyglot.issues.errors import AssigneeNotFoundError, InvalidStatusTransitionError, LabelNotFoundError
from polyglot.issues.models import Issue
from polyglot.issues.schemas import IssueCreate, IssueRead, IssueStatus, IssueUpdate
from polyglot.labels.models import Label
from polyglot.users.models import User

ALLOWED_TRANSITIONS = {
    "open": {"in-progress"},
    "in-progress": {"closed"},
    "closed": {"open"},
}

def to_issue_read(issue: Issue) -> IssueRead:
    return IssueRead(
        id=issue.id,
        project_id=issue.project_id,
        title=issue.title,
        description=issue.description,
        status=issue.status, # type: ignore
        label_ids=[label.id for label in issue.labels],
        assignee_ids=[user.id for user in issue.assignees],
        created_at=issue.created_at,
        updated_at=issue.updated_at,
    )


def get_issues(session: Session, project_id: UUID, limit: int, cursor: UUID | None = None, status: IssueStatus | None = None, label: str | None = None, assignee: UUID | None = None) -> Page[IssueRead]:
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
    if status:
        stmt = stmt.where(Issue.status == status)
    if label:
        stmt = stmt.where(Issue.labels.any(Label.name == label))
    if assignee:
        stmt = stmt.where(Issue.assignees.any(User.id == assignee))
    response = session.exec(stmt.limit(limit)).all()
    return Page(
        items=[to_issue_read(issue) for issue in response],
        pagination=Pagination(limit=limit, next_cursor=str(response[-1].id) if len(response) == limit else None),
    )

def get_issue(session: Session, issue_id: UUID) -> IssueRead | None:
    issue = session.get(Issue, issue_id)
    if not issue:
        return None
    return to_issue_read(issue)

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

def update_issue(session: Session, issue_id: UUID, data: IssueUpdate) -> IssueRead | None:
    issue = session.get(Issue, issue_id)
    if not issue:
        return None

    if data.status is not None and data.status != issue.status:
        if data.status not in ALLOWED_TRANSITIONS[issue.status]:
            raise InvalidStatusTransitionError(f"Invalid status transition from '{issue.status}' to '{data.status}'")

    if data.label_ids is not None:
        labels = _fetch_by_ids(session, Label, data.label_ids)
        missing_labels = set(data.label_ids) - {label.id for label in labels}
        if missing_labels:
            raise LabelNotFoundError(f"Labels not found: {_join(missing_labels)}")
        issue.labels = labels

    if data.assignee_ids is not None:
        users = _fetch_by_ids(session, User, data.assignee_ids)
        missing_users = set(data.assignee_ids) - {user.id for user in users}
        if missing_users:
            raise AssigneeNotFoundError(f"Assignees not found: {_join(missing_users)}")
        issue.assignees = users

    for key, value in data.model_dump(exclude_unset=True, exclude={"label_ids", "assignee_ids"}).items():
        setattr(issue, key, value)

    issue.updated_at = datetime.now(timezone.utc)
    session.add(issue)
    session.commit()
    session.refresh(issue)
    return to_issue_read(issue)

def assign_user_to_issue(session: Session, issue_id: UUID, user_id: UUID) -> bool:
    issue = session.get(Issue, issue_id)
    if not issue:
        return False

    user = session.get(User, user_id)
    if not user:
        raise AssigneeNotFoundError(f"Assignee not found: {user_id}")

    if user not in issue.assignees:
        issue.assignees.append(user)

    session.add(issue)
    session.commit()
    return True

def remove_user_from_issue(session: Session, issue_id: UUID, user_id: UUID) -> bool:
    issue = session.get(Issue, issue_id)
    if not issue:
        return False

    user = session.get(User, user_id)
    if not user:
        raise AssigneeNotFoundError(f"Assignee not found: {user_id}")

    if user in issue.assignees:
        issue.assignees.remove(user)

    session.add(issue)
    session.commit()
    return True

def _fetch_by_ids(session: Session, model, ids: list[UUID]) -> list:
    if not ids:
        return []
    return list(session.exec(select(model).where(model.id.in_(ids))).all())

def _join(ids: set[UUID]) -> str:
    return ", ".join(sorted(str(i) for i in ids))
