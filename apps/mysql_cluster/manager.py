from fastapi import FastAPI, Request
import requests
import uvicorn
from http import HTTPStatus
from datetime import datetime
import db
import json
from pydantic import BaseModel

# Request body
class New_Actor_Request(BaseModel):
    first_name: str
    last_name: str


# Create FastAPI app
app = FastAPI()

with open("workers.json", "r") as f:
    workers_data = json.load(f)
    workers = [worker_data["Private IP"] for worker_data in workers_data]

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
    # Add time
    time = datetime.now().date()
    data = {
        "first_name": actor_request.first_name,
        "last_name": actor_request.last_name,
        "time": time.strftime("%m/%d/%Y"),
    }

    # Replicate the write on all workers
    for worker in workers:
        requests.post(
            url=f"http://{worker}",
            json=data,
        )

    db.add_actor(actor_request.first_name, actor_request.last_name, time)
    print(f"[{instance_id}] - [WRITE] Wrote {data.values()} to database")
    return


@app.post("/direct", status_code=HTTPStatus.CREATED)
async def treat_request(actor_request: New_Actor_Request):
    time = datetime.now().date()
    db.add_actor(
        actor_request.first_name, actor_request.last_name, time
    )
    print(f"[{instance_id}] - [WRITE] Wrote {[actor_request.first_name, actor_request.last_name, time]} to database")
    return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
