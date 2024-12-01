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


@app.get("/health", status_code=HTTPStatus.OK)
async def health_check(request: Request):
    return


@app.get("/")
async def treat_request():
    return db.fetch_actors()


@app.post("/", status_code=HTTPStatus.CREATED)
async def treat_request(actor_request: New_Actor_Request, request: Request):
    # Add time
    time = datetime.now().date()

    # Replicate the write on all workers
    for worker in workers:
        requests.post(
            url=f"http://{worker}",
            json={
                "first_name": actor_request.first_name,
                "last_name": actor_request.last_name,
                "time": time.strftime("%m/%d/%Y"),
            },
        )

    db.add_actor(actor_request.first_name, actor_request.last_name, time)
    return


@app.post("/direct", status_code=HTTPStatus.CREATED)
async def treat_request(actor_request: New_Actor_Request):
    db.add_actor(
        actor_request.first_name, actor_request.last_name, datetime.now().date()
    )
    return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
