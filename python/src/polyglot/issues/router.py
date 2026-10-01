from fastapi import APIRouter

router = APIRouter(prefix="/issues", tags=["issues"])

@router.get("/{issue_id}")
def get_issue(issue_id: str):
    return {"Hello": issue_id}

@router.patch("/{issue_id}")
def update_issue(issue_id: str):
    return {"Hello": issue_id}

@router.get("/{issue_id}/comments")
def get_issue_comments(issue_id: str):
    return {"Hello": issue_id}

@router.post("/{issue_id}/comments")
def create_issue_comment(issue_id: str):
    return {"Hello": issue_id}

@router.put("/{issue_id}/assignees/{user_id}")
def update_issue_assignee(issue_id: str, user_id: str):
    return {"Hello": issue_id, "World": user_id}

@router.delete("/{issue_id}/assignees/{user_id}")
def delete_issue_assignee(issue_id: str, user_id: str):
    return {"Hello": issue_id, "World": user_id}