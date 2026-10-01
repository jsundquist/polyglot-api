from fastapi import APIRouter

router = APIRouter(prefix="/comments", tags=["comments"])

@router.patch("/{comment_id}")
def update_comment(comment_id: str):
    return {"Hello": comment_id}

@router.delete("/{comment_id}")
def delete_comment(comment_id: str):
    return {"Hello": comment_id}