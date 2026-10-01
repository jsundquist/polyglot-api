from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/")
def get_projects():
    return {"Hello": "World"}

@router.post("/")
def create_project():
    return {"Hello": "World"}

@router.get("//{project_id}")
def get_project(project_id: str):
    return {"Hello": project_id}

@router.patch("//{project_id}")
def update_project(project_id: str):
    return {"Hello": project_id}

@router.get("//{project_id}/issues")
def get_project_issues(project_id: str):
    return {"Hello": project_id}

@router.post("//{project_id}/issues")
def create_project_issues(project_id: str):
    return {"Hello": project_id}