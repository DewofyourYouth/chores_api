from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from mongo_queries import handlers
from pydantic import BaseModel


load_dotenv()

app = FastAPI()


class PointsObject(BaseModel):
    kid: str
    points: int


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/kid-score/{kid_name}", status_code=200)
def get_kid_score(kid_name: str, response: Response) -> PointsObject:
    points = handlers.calculate_points(kid_name)
    if not points:
        response.status_code = status.HTTP_204_NO_CONTENT
    kid_list = kid_name.split(" ")

    return PointsObject(
        kid=" ".join(map(lambda x: x.capitalize(), kid_list)),
        points=points,
    )
