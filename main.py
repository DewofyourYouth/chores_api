import pprint
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from mongo_queries import chore
from pydantic import BaseModel
from mongo_queries.kids import Kid, add_kid_to_mongo
from mongo_queries import client


load_dotenv()

app = FastAPI()


class PointsObject(BaseModel):
    kid: str
    points: int


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/kids/")
def get_kids():
    db = client.chores
    kids = [
        Kid(firstName=k["firstName"], lastName=k["lastName"], yearBorn=k["yearBorn"])
        for k in db.kids.find()
    ]
    return kids


@app.get("/kids/{kid_name}")
def get_kid(kid_name: str):
    db = client.chores
    kid = db.kids.find_one({"firstName": kid_name})
    pprint.pprint(kid)
    return {
        "name": kid["firstName"],
    }


@app.get("/kid-score/{kid_name}", status_code=200)
def get_kid_score(kid_name: str, response: Response) -> PointsObject:
    points = chore.calculate_points(kid_name)
    if not points:
        response.status_code = status.HTTP_204_NO_CONTENT
    kid_list = kid_name.split(" ")

    return PointsObject(
        kid=" ".join(map(lambda x: x.capitalize(), kid_list)),
        points=points,
    )


@app.post("/new-kid/")
def create_kid(kid: Kid) -> Kid:
    return add_kid_to_mongo(kid)
