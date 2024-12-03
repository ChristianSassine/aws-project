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

with open("ID", "r") as f:
    instance_id = f.read().rstrip('\n')

@app.get("/health", status_code=HTTPStatus.OK)
async def health_check():
    return


@app.get("/")
async def treat_request():
    last_actors = db.fetch_actors()
    print(f"[{instance_id}] - [READ] Fetched actors from database : {last_actors}")
    return last_actors


@app.post("/", status_code=HTTPStatus.CREATED)
async def treat_request(actor_request: New_Actor_Request):
    time = datetime.strptime(actor_request.time, "%m/%d/%Y").date()
    db.add_actor(actor_request.first_name, actor_request.last_name, time)
    print(
        f"[{instance_id}] - [WRITE] Wrote {[actor_request.first_name, actor_request.last_name, time]} to database"
    )
    return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
