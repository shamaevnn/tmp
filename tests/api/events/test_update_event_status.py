import pytest

from app.api.events.schemas import GetEvent
from app.types import BetStatus

pytestmark = pytest.mark.asyncio


async def test_success_update_event_status(async_client, random_event: GetEvent):
    # создаем N ставок
    n_bets = 10
    for _ in range(n_bets):
        params = {"event_id": random_event.id, "amount": 2.00}
        await async_client.post("/bets", json=params)

    # обновляем статус события
    new_status = BetStatus.LOSE
    await async_client.put(f"/events/{random_event.id}", json={"status": new_status})

    # получаем все ставки и проверяем, что их статус изменился
    response = await async_client.get("/bets")
    resp = response.json()

    assert resp["total"] == n_bets
    bets = resp["items"]
    for bet in bets:
        assert bet["status"] == new_status
