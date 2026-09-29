"""
Deterministic, spec-driven end-to-end flows against a running implementation.

This is the reference "golden path" for the API - every language
implementation should be able to run this file, unmodified, against its own
server (set CONTRACT_TEST_BASE_URL) and pass. It complements test_schema.py,
which fuzzes the spec for schema/status-code conformance rather than
asserting on real business flows.
"""

import uuid
from http import HTTPStatus

import requests


def unique_key(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def test_project_lifecycle(session, base_url):
    key = unique_key("contract-project")

    resp = session.post(f"{base_url}/projects", json={"name": "Contract Project", "key": key})
    assert resp.status_code == HTTPStatus.CREATED, resp.text
    project = resp.json()
    assert project["key"] == key
    assert project["status"] == "active"
    project_id = project["id"]

    resp = session.post(f"{base_url}/projects", json={"name": "Duplicate", "key": key})
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    resp = session.get(f"{base_url}/projects/{project_id}")
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["id"] == project_id

    resp = session.get(f"{base_url}/projects/{uuid.uuid4()}")
    assert resp.status_code == HTTPStatus.NOT_FOUND
    body = resp.json()
    assert "code" in body
    assert "message" in body

    resp = session.patch(f"{base_url}/projects/{project_id}", json={"description": "updated"})
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["description"] == "updated"

    resp = session.patch(f"{base_url}/projects/{project_id}", json={"status": "archived"})
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["status"] == "archived"

    resp = session.patch(f"{base_url}/projects/{project_id}", json={"status": "archived"})
    assert resp.status_code == HTTPStatus.CONFLICT


def test_label_lifecycle(session, base_url):
    name = unique_key("contract-label")

    resp = session.post(f"{base_url}/labels", json={"name": name, "color": "#ff0000"})
    assert resp.status_code == HTTPStatus.CREATED, resp.text
    label = resp.json()

    resp = session.post(f"{base_url}/labels", json={"name": name, "color": "#00ff00"})
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    resp = session.get(f"{base_url}/labels")
    assert resp.status_code == HTTPStatus.OK
    body = resp.json()
    assert "items" in body
    assert "pagination" in body

    resp = session.delete(f"{base_url}/labels/{label['id']}")
    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_issue_and_comment_lifecycle(session, base_url, seeded_user):
    project = session.post(
        f"{base_url}/projects", json={"name": "Issue Project", "key": unique_key("issue-project")}
    ).json()
    project_id = project["id"]

    label = session.post(
        f"{base_url}/labels", json={"name": unique_key("issue-label"), "color": "#123456"}
    ).json()

    resp = session.post(
        f"{base_url}/projects/{project_id}/issues",
        json={"title": "Bug", "label_ids": [label["id"]], "assignee_ids": [seeded_user]},
    )
    assert resp.status_code == HTTPStatus.CREATED, resp.text
    issue = resp.json()
    assert issue["label_ids"] == [label["id"]]
    assert issue["assignee_ids"] == [seeded_user]
    issue_id = issue["id"]

    resp = session.post(
        f"{base_url}/projects/{project_id}/issues",
        json={"title": "Bad label ref", "label_ids": [str(uuid.uuid4())]},
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    resp = session.get(f"{base_url}/projects/{project_id}/issues")
    assert resp.status_code == HTTPStatus.OK
    listed = resp.json()
    assert "items" in listed
    assert "pagination" in listed
    assert any(i["id"] == issue_id for i in listed["items"])

    resp = session.patch(f"{base_url}/issues/{issue_id}", json={"status": "in_progress"})
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["status"] == "in_progress"

    resp = session.patch(f"{base_url}/issues/{issue_id}", json={"status": "open"})
    assert resp.status_code == HTTPStatus.CONFLICT

    resp = session.post(
        f"{base_url}/issues/{issue_id}/comments",
        json={"body": "Repro'd locally.", "author_id": seeded_user},
    )
    assert resp.status_code == HTTPStatus.CREATED, resp.text
    comment = resp.json()
    assert comment["issue_id"] == issue_id

    resp = session.get(f"{base_url}/issues/{issue_id}/comments")
    assert resp.status_code == HTTPStatus.OK
    assert any(c["id"] == comment["id"] for c in resp.json()["items"])

    resp = session.patch(f"{base_url}/comments/{comment['id']}", json={"body": "updated body"})
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["body"] == "updated body"

    resp = session.delete(f"{base_url}/comments/{comment['id']}")
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = session.put(f"{base_url}/issues/{issue_id}/assignees/{seeded_user}")
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = session.put(f"{base_url}/issues/{issue_id}/assignees/{seeded_user}")
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = session.delete(f"{base_url}/issues/{issue_id}/assignees/{seeded_user}")
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = session.delete(f"{base_url}/issues/{issue_id}/assignees/{seeded_user}")
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = session.put(f"{base_url}/issues/{issue_id}/assignees/{uuid.uuid4()}")
    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_webhook_lifecycle(session, base_url):
    project = session.post(
        f"{base_url}/projects", json={"name": "Webhook Project", "key": unique_key("webhook-project")}
    ).json()
    project_id = project["id"]

    resp = session.post(
        f"{base_url}/projects/{project_id}/webhooks",
        json={"url": "https://example.com/hook", "events": ["issue.created"], "secret": "s3cr3t"},
    )
    assert resp.status_code == HTTPStatus.CREATED, resp.text
    webhook = resp.json()
    assert "secret" not in webhook

    resp = session.get(f"{base_url}/projects/{project_id}/webhooks")
    assert resp.status_code == HTTPStatus.OK
    assert all("secret" not in w for w in resp.json())

    resp = session.get(f"{base_url}/webhooks/{webhook['id']}")
    assert resp.status_code == HTTPStatus.OK
    assert "secret" not in resp.json()

    resp = session.delete(f"{base_url}/webhooks/{webhook['id']}")
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = session.get(f"{base_url}/webhooks/{webhook['id']}")
    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_auth_is_required(base_url):
    resp = requests.get(f"{base_url}/projects")
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    resp = requests.get(f"{base_url}/projects", headers={"X-API-Key": "not-a-real-key"})
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
