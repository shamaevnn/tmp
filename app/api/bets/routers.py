import asyncio
from http import HTTPStatus
from math import ceil
from fastapi import APIRouter, Query
from fastapi_pagination import Page


from app.api.bets.schemas import CreateBet, CreateBetResponse, GetBet
from app.api.errors import BadRequestCreatingBet
from app.db.models.bets.handlers import count_all_bets, create_new_bet, get_bets

bets_router = APIRouter(tags=["Bets"], prefix="/bets")


@bets_router.post("", response_model=CreateBetResponse, status_code=HTTPStatus.CREATED)
async def new_bet(
    params: CreateBet,
) -> CreateBetResponse:
    bet_id, err = await create_new_bet(params=params)
    if err:
        raise BadRequestCreatingBet(msg=err)
    assert bet_id is not None
    res: CreateBetResponse = CreateBetResponse.parse_obj({"id": bet_id})
    return res


@bets_router.get("", response_model=Page[GetBet])
async def get_paginated_bets(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=3, le=30),
) -> Page[GetBet]:
    total_bets, bets = await asyncio.gather(*[count_all_bets, get_bets(page=page, size=size)])
    total_pages = ceil(total_bets / size)
    return Page(total=total_bets, page=page, size=size, items=bets, pages=total_pages)
