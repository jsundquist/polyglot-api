import secrets
from uuid import UUID

from sqlmodel import Session, select

from polyglot.webhooks.models import WebhookSubscription
from polyglot.webhooks.schemas import WebhookCreate


def list_webhooks(session: Session, project_id: UUID) -> list[WebhookSubscription]:
    stmt = (
        select(WebhookSubscription)
        .where(WebhookSubscription.project_id == project_id)
        .order_by(WebhookSubscription.created_at.desc(), WebhookSubscription.id)  # type: ignore
    )
    return list(session.exec(stmt).all())

def get_webhook(session: Session, webhook_id: UUID) -> WebhookSubscription | None:
    return session.get(WebhookSubscription, webhook_id)

def create_webhook(session: Session, project_id: UUID, data: WebhookCreate) -> WebhookSubscription:
    webhook = WebhookSubscription(
        project_id=project_id,
        url=str(data.url),
        events=[event.value for event in data.events],
        # The DB requires a secret; generate one when the caller doesn't supply their own.
        secret=data.secret or f"whsec_{secrets.token_urlsafe(32)}",
    )
    session.add(webhook)
    session.commit()
    session.refresh(webhook)
    return webhook

def delete_webhook(session: Session, webhook_id: UUID) -> bool:
    webhook = get_webhook(session, webhook_id)
    if not webhook:
        return False
    session.delete(webhook)
    session.commit()
    return True
