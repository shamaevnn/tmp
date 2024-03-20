import pytest

from app.db.models.events.handlers import event_exists

pytestmark = pytest.mark.asyncio


async def test_success_create_event(async_client):
    params = {"title": "Test"}
    response = await async_client.post("/events", json=params)
    assert response.status_code == 201
    event_id = response.json()["id"]
    assert await event_exists(event_id), "event doesn't exist in DB"
