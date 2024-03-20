import pytest

from app.api.events.schemas import GetEvent
from app.types import BetStatus

pytestmark = pytest.mark.asyncio


async def test_success_get_bets(async_client, random_event: GetEvent):
    # создаем ставку
    params = {"event_id": random_event.id, "amount": 2.00}
    response = await async_client.post("/bets", json=params)
    resp = response.json()
    bet_id = resp["id"]

    # получаем все ставки
    response = await async_client.get("/bets")
    resp = response.json()

    assert resp["total"] == 1
    items = resp["items"]
    assert len(items) == 1, "Должна быть создана только 1 ставка"
    bet = items[0]
    assert bet["status"] == BetStatus.IN_PROGRESS
    assert bet["id"] == bet_id
