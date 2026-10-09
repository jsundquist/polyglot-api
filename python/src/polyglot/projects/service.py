from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from polyglot.common.pagination import Page, Pagination
from polyglot.projects.errors import DuplicateProjectKeyError, ProjectArchiveError
from polyglot.projects.models import Project
from polyglot.projects.schemas import ProjectCreate, ProjectRead, ProjectUpdate


def project_list(session: Session, limit: int, cursor: UUID | None = None) -> Page[ProjectRead]:
    stmt = select(Project).order_by(Project.id)
    if cursor:
        stmt = stmt.where(Project.id > cursor)
    response = session.exec(stmt.limit(limit)).all()
    return Page(items=[ProjectRead.model_validate(project) for project in response], pagination=Pagination(limit=limit, next_cursor=str(response[-1].id) if len(response) == limit else None))

def get_project(session: Session, id: UUID) -> Project | None:
    return session.get(Project, id)

def create_project(session: Session, data: ProjectCreate) -> Project:
    project = Project.model_validate(data)
    project.status = "active"
    session.add(project)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise DuplicateProjectKeyError(f"Project key '{project.key}' already exists") from e

    session.refresh(project)
    return project

def update_project(session: Session, id: UUID, data: ProjectUpdate) -> Project | None:
    project = get_project(session, id)
    if not project:
        return None

    if project.status == "archived" and data.status is not None:
        raise ProjectArchiveError("Cannot change the status of an archived project")


    project.updated_at = datetime.now(UTC)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project