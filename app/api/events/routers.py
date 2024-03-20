from http import HTTPStatus

from fastapi import APIRouter
from app.api.events.schemas import GetEvent, CreateEvent, UpdateEventStatus

from app.api.errors import BadRequestCreatingEvent, EventNotExist
from app.db.models.bets.handlers import update_status_of_all_bets_for_event
from app.db.models.events.handlers import create_event, event_exists

events_router = APIRouter(tags=["Events"], prefix="/events")


@events_router.post("", response_model=GetEvent, status_code=HTTPStatus.CREATED)
async def create_new_event(params: CreateEvent) -> GetEvent:
    """
    Creating new user
    Checking if user is already exists with such username and email
    """

    event, err = await create_event(params=params)
    if err:
        raise BadRequestCreatingEvent(msg=err)
    assert event is not None

    return event


@events_router.put("/{event_id}", status_code=HTTPStatus.OK)
async def update_event_status(event_id: str, params: UpdateEventStatus) -> None:
    if not await event_exists(event_id=event_id):
        raise EventNotExist(event_id=event_id)
    await update_status_of_all_bets_for_event(event_id=event_id, new_bet_status=params.status)
