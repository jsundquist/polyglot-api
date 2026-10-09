from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from polyglot.common.pagination import Page
from polyglot.db.db import SessionDep
from polyglot.issues import service as issue_service
from polyglot.issues.errors import AssigneeNotFoundError, LabelNotFoundError
from polyglot.issues.schemas import IssueCreate, IssueRead, IssueStatus
from polyglot.projects import service
from polyglot.projects.errors import DuplicateProjectKeyError, ProjectArchiveError
from polyglot.projects.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=Page[ProjectRead])
def get_projects(session: SessionDep, limit: int = Query(20, ge=1, le=100), cursor: UUID | None = None):
    return service.project_list(session, limit, cursor)

@router.post("/", status_code=201, response_model=ProjectRead)
def create_project(session: SessionDep, data: ProjectCreate):
    try:
        return service.create_project(session, data)
    except DuplicateProjectKeyError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/{project_id}", response_model=ProjectRead)
def get_project(session: SessionDep, project_id: UUID):
    project = service.get_project(session, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(session: SessionDep, project_id: UUID, data: ProjectUpdate):
    try:
        project = service.update_project(session, project_id, data)
    except ProjectArchiveError:
        raise HTTPException(status_code=409, detail="Project is already archived, cannot change the status")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.get("/{project_id}/issues", response_model=Page[IssueRead])
def get_project_issues(session: SessionDep, project_id: UUID, limit: int = Query(20, ge=1, le=100), cursor: UUID | None = None, status: IssueStatus | None = None, label: str | None = None, assignee: UUID | None = None):
    project = service.get_project(session, project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return issue_service.get_issues(session, project_id, limit, cursor, status=status, label=label, assignee=assignee)

@router.post("/{project_id}/issues", status_code=201, response_model=IssueRead)
def create_project_issues(session: SessionDep, project_id: UUID, data: IssueCreate):
    project = service.get_project(session, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        return issue_service.create_issue(session, project_id, data)
    except (LabelNotFoundError, AssigneeNotFoundError) as e:
        raise HTTPException(status_code=422, detail=str(e))
