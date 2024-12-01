from fastapi import FastAPI, Request
import uvicorn
from http import HTTPStatus
import db
from pydantic import BaseModel
from datetime import datetime


# Request body
class New_Actor_Request(BaseModel):
    first_name: str
    last_name: str
    time: str


# Create FastAPI app
app = FastAPI()


@app.get("/health", status_code=HTTPStatus.OK)
async def health_check():
    return


@app.get("/")
async def treat_request():
    return db.fetch_actors()


@app.post("/", status_code=HTTPStatus.CREATED)
async def treat_request(actor_request: New_Actor_Request, request: Request):
    body = await request.body()
    print(body)
    time = datetime.strptime(actor_request.time, "%m/%d/%Y").date()
    db.add_actor(actor_request.first_name, actor_request.last_name, time)
    return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
