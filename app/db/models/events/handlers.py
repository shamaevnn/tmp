from asyncpg import NotNullViolationError, UniqueViolationError
from databases.backends.postgres import Record
from pydantic import ValidationError
from sqlalchemy import insert, literal_column, select


from app.api.events.schemas import CreateEvent, GetEvent
from app.db.models.events.schemas import Event


from app.db.base import database


async def create_event(params: CreateEvent) -> tuple[GetEvent | None, str | None]:
    """
    creates new event
    returns event and optional error
    """
    values = params.dict()

    query = (
        insert(Event)
        .values(**values)
        .returning(
            literal_column("id"),
            literal_column("created_at"),
        )
    )
    transaction = await database.transaction()
    try:
        row: Record = await database.fetch_one(query)

        event_id, created_at = row._mapping.values()
        event: GetEvent = GetEvent.construct(
            **dict(
                id=event_id,
                created_at=created_at,
                **values,
            )
        )
    except (NotNullViolationError, UniqueViolationError) as exc:
        await transaction.rollback()
        return None, str(exc)
    except ValidationError as exc:
        await transaction.rollback()
        return None, str(exc)
    else:
        await transaction.commit()
        return event, None


async def event_exists(event_id: str) -> bool:
    query = select([Event.id]).where(Event.id == event_id).limit(1)
    res: Record = await database.fetch_one(query)
    return bool(res)
