from dataclasses import dataclass
from enum import Enum
import os
import re
from typing import Protocol
from urllib import response

from dotenv import load_dotenv
from more_itertools import flatten
from pymongo import MongoClient

DAILY_CHORE_VAL = 1
ALTERNATING_CHORE_VAL = 3

load_dotenv()

password = os.getenv("PASSWORD")
mongo_user = os.getenv("MONGO_USER")
mongo_uri = f"mongodb+srv://{mongo_user}:{password}@cluster0.iep8o.azure.mongodb.net/chores?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)


class DoneState(Enum):
    DONE = "done"
    NOT_DONE = "notDone"
    UNMARKED = "unmarked"


class Chore(Protocol):
    def score(self) -> int:
        ...


@dataclass
class AlternatingChore:
    chore: str
    done_state: DoneState

    def score(self) -> int:
        if self.done_state == DoneState.DONE:
            return ALTERNATING_CHORE_VAL
        return 0


@dataclass
class DailyChore:
    chore: str
    done_state: DoneState

    def score(self) -> int:
        match (self.done_state):
            case DoneState.UNMARKED:
                return 0
            case DoneState.DONE:
                return DAILY_CHORE_VAL
            case DoneState.NOT_DONE:
                return 0 - DAILY_CHORE_VAL


def get_chore(
    is_alternating: bool,
    chore: str,
    done: DoneState,
) -> Chore:
    return AlternatingChore(chore, done) if is_alternating else DailyChore(chore, done)


def calculate_points(kid_name: str) -> list[dict[str, int]] | None:
    kid_regex = re.compile(kid_name, re.IGNORECASE)
    db = client.chores
    chores = list(db.chores.find({"kidName": kid_regex}))
    if len(chores) == 0:
        return None
    chores = list(flatten([c["chores"] for c in chores]))
    return sum(
        [
            get_chore(c.get("isAlternating"), c["chore"], DoneState(c["done"])).score()
            for c in chores
        ]
    )
