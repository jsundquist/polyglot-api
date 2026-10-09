from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from polyglot.comments import service as comment_service
from polyglot.comments.schemas import CommentCreate, CommentRead
from polyglot.common.pagination import Page
from polyglot.db.db import SessionDep
from polyglot.issues import service
from polyglot.issues.errors import (
    AssigneeNotFoundError,
    InvalidStatusTransitionError,
    LabelNotFoundError,
)
from polyglot.issues.schemas import IssueRead, IssueUpdate

router = APIRouter(prefix="/issues", tags=["issues"])

@router.get("/{issue_id}", response_model=IssueRead)
def get_issue(session: SessionDep, issue_id: UUID):
    issue = service.get_issue(session, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.patch("/{issue_id}", response_model=IssueRead)
def update_issue(session: SessionDep, issue_id: UUID, data: IssueUpdate):
    try:
        issue = service.update_issue(session, issue_id, data)
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        return issue
    except InvalidStatusTransitionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except LabelNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AssigneeNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{issue_id}/comments", response_model=Page[CommentRead])
def get_issue_comments(session: SessionDep, issue_id: UUID, limit: int = Query(20, ge=1, le=100), cursor: UUID | None = None):
    response = comment_service.get_comments(session, issue_id, limit, cursor)
    if not response:
        raise HTTPException(status_code=404, detail="Issue not found")
    return response

@router.post("/{issue_id}/comments", response_model=CommentRead, status_code=201)
def create_issue_comment(session: SessionDep, issue_id: UUID, data: CommentCreate):
    try:
        response = comment_service.create_comment(session, issue_id, data)
    except AssigneeNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if not response:
        raise HTTPException(status_code=404, detail="Issue not found")
    return response

@router.put("/{issue_id}/assignees/{user_id}", status_code=204)
def update_issue_assignee(session: SessionDep, issue_id: UUID, user_id: UUID):
    try:
        response = service.assign_user_to_issue(session, issue_id, user_id)
        if not response:
            raise HTTPException(status_code=404, detail="Issue or user not found")
    except AssigneeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{issue_id}/assignees/{user_id}", status_code=204)
def delete_issue_assignee(session: SessionDep, issue_id: UUID, user_id: UUID):
    try:
        response = service.remove_user_from_issue(session, issue_id, user_id)
        if not response:
            raise HTTPException(status_code=404, detail="Issue or user not found")
    except AssigneeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))