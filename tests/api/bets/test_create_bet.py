import pytest

from app.api.events.schemas import GetEvent
from app.db.models.bets.handlers import bet_exists
from tests.utils import get_random_string

pytestmark = pytest.mark.asyncio


async def test_success_create_bet(async_client, random_event: GetEvent):
    params = {"event_id": random_event.id, "amount": 2.00}
    response = await async_client.post("/bets", json=params)
    assert response.status_code == 201

    resp = response.json()
    bet_id = resp["id"]
    assert await bet_exists(bet_id), "bet doesn't exist in DB"


@pytest.mark.parametrize("amount", [0, -2, -1])
async def test_cant_create_with_wrong_amount(async_client, random_event, amount):
    params = {"event_id": random_event.id, "amount": amount}
    response = await async_client.post("/bets", json=params)
    assert response.status_code == 422


async def test_cant_create_with_wrong_event_id(async_client):
    params = {"event_id": get_random_string(length=64), "amount": 2.00}
    response = await async_client.post("/bets", json=params)
    assert response.status_code == 404, response.text
