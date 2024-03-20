from enum import Enum


class BetStatus(str, Enum):
    WIN = "WIN"
    IN_PROGRESS = "IN_PROGRESS"
    LOSE = "LOSE"
