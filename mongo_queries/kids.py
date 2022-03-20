from shutil import ExecError
from pydantic import BaseModel, validator, ValidationError

from mongo_queries import *
import humps


class Kid(BaseModel):
    first_name: str
    last_name: str
    year_born: int

    @validator("first_name")
    def first_name_must_be_at_least_two_chars(cls, v):
        if len(v) < 2:
            raise ValidationError("First name must be ar least two characters")
        return v

    @validator("last_name")
    def last_name_must_be_at_least_two_chars(cls, v):
        if len(v) < 2:
            raise ValidationError("Last name must be ar least two characters")
        return v

    class Config:
        alias_generator = humps.camelize


def add_kid_to_mongo(kid: Kid) -> Kid:
    db = client.chores
    try:
        db.kids.insert_one(kid.dict(by_alias=True))
        return kid
    except Exception as e:
        return e
