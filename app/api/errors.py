from http import HTTPStatus

from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, user_param: str, status_code: int = HTTPStatus.NOT_FOUND) -> None:
        super().__init__(
            status_code=status_code,
            detail=f"User {user_param} is not found.",
        )


class UserAlreadyExist(HTTPException):
    def __init__(self, param: str) -> None:
        msg = f"User with {param=} already exists."
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=msg)


class BadRequestCreatingEvent(HTTPException):
    def __init__(self, msg: str) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=msg)


class BadRequestCreatingBet(HTTPException):
    def __init__(self, msg: str) -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=msg)


class EventNotExist(HTTPException):
    def __init__(self, event_id: str) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=f"Event {event_id} not found")
