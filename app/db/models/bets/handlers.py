from asyncpg import NotNullViolationError, UniqueViolationError
from sqlalchemy import select, insert, literal_column, update, func
from app.api.bets.schemas import CreateBet, GetBet
from app.api.events.schemas import UpdateEventStatusEnum
from app.db.models.bets.schemas import Bet
from app.db.base import database

from app.types import BetStatus


async def get_bets(page: int, size: int) -> list[GetBet]:
    query = select(Bet).limit(size).offset((page - 1) * size)
    fetched = await database.fetch_all(query)
    return [GetBet.parse_obj(x) for x in fetched or []]


async def create_new_bet(params: CreateBet) -> tuple[str | None, str | None]:
    """
    creates new bet
    returns its id and optional error
    """
    values = params.dict()
    values["status"] = BetStatus.IN_PROGRESS.value

    query = insert(Bet).values(**values).returning(literal_column("id"))
    transaction = await database.transaction()
    try:
        bet_id: str = await database.fetch_val(query)
        # bet_id = row._mapping.values()
    except (NotNullViolationError, UniqueViolationError) as exc:
        await transaction.rollback()
        return None, str(exc)
    else:
        await transaction.commit()
        return bet_id, None


async def update_status_of_all_bets_for_event(
    event_id: str, new_bet_status: UpdateEventStatusEnum
) -> None:
    values = {"status": new_bet_status.value}
    query = update(Bet).where(Bet.event_id == event_id).values(values)
    await database.execute(query)


async def count_all_bets() -> int:
    query = select(func.count()).select_from(Bet)
    count: int = await database.execute(query)
    return count
