from dataclasses import dataclass
from enum import Enum
import re
from typing import Protocol
from mongo_queries import *

from more_itertools import flatten

DAILY_CHORE_VAL = 1
ALTERNATING_CHORE_VAL = 3


class DoneState(Enum):
    DONE = "done"
    NOT_DONE = "notDone"
    UNMARKED = "unmarked"


class Chore(Protocol):
    def score(self) -> int:
        ...


@dataclass
class AlternatingChore(Chore):
    chore: str
    done_state: DoneState

    def score(self) -> int:
        if self.done_state == DoneState.DONE:
            return ALTERNATING_CHORE_VAL
        return 0


@dataclass
class DailyChore(Chore):
    chore: str
    done_state: DoneState

    def score(self) -> int:
        if self.done_state == DoneState.DONE:
            return DAILY_CHORE_VAL
        elif self.done_state == DoneState.NOT_DONE:
            return 0 - DAILY_CHORE_VAL
        return 0


def get_chore(
    is_alternating: bool,
    chore: str,
    done: DoneState,
) -> Chore:
    return AlternatingChore(chore, done) if is_alternating else DailyChore(chore, done)


def calculate_points(kid_name: str) -> int:
    kid_regex = re.compile(kid_name, re.IGNORECASE)
    db = client.chores
    chores = list(db.chores.find({"kidName": kid_regex}))
    if len(chores) == 0:
        return 0
    chores = list(flatten([c["chores"] for c in chores]))
    return sum(
        [
            get_chore(c.get("isAlternating"), c["chore"], DoneState(c["done"])).score()
            for c in chores
        ]
    )
