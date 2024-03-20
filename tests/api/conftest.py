import pytest

from app.api.bets.schemas import GetBet
from app.api.events.schemas import CreateEvent, GetEvent
from app.db.models.events.handlers import create_event
from tests.utils import get_random_string


@pytest.fixture(scope="function")
async def random_event() -> GetEvent:
    params = CreateEvent(title=get_random_string(length=32))
    event, _ = await create_event(params)
    return event
