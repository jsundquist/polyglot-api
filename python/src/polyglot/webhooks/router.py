from fastapi import APIRouter, HTTPException
from uuid import UUID

from polyglot.db.db import SessionDep
from polyglot.projects import service as project_service
from polyglot.webhooks import service
from polyglot.webhooks.schemas import WebhookCreate, WebhookRead

router = APIRouter(tags=["webhooks"])

@router.get("/projects/{project_id}/webhooks", response_model=list[WebhookRead])
def get_project_webhooks(session: SessionDep, project_id: UUID):
    if not project_service.get_project(session, project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    return service.list_webhooks(session, project_id)

@router.post("/projects/{project_id}/webhooks", status_code=201, response_model=WebhookRead)
def create_project_webhook(session: SessionDep, project_id: UUID, data: WebhookCreate):
    if not project_service.get_project(session, project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    return service.create_webhook(session, project_id, data)

@router.get("/webhooks/{webhook_id}", response_model=WebhookRead)
def get_webhook(session: SessionDep, webhook_id: UUID):
    webhook = service.get_webhook(session, webhook_id)

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook

@router.delete("/webhooks/{webhook_id}", status_code=204)
def delete_webhook(session: SessionDep, webhook_id: UUID):
    if not service.delete_webhook(session, webhook_id):
        raise HTTPException(status_code=404, detail="Webhook not found")
