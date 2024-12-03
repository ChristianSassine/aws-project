from fastapi import FastAPI, Request
import requests
import uvicorn
import json
import random
from http import HTTPStatus
import heapq
import datetime

# Create FastAPI app
app = FastAPI()

with open("workers.json", "r") as f:
    workers_data = json.load(f)
    workers = [worker_data["Private IP"] for worker_data in workers_data]

with open("manager.json", "r") as f:
    manager_data = json.load(f)
    manager = manager_data["Private IP"]

# We'll passively mesure the ping/latency by using incoming requests
heap = [[datetime.timedelta(), worker] for worker in workers] + [[datetime.timedelta(), manager]]

@app.get("/health", status_code=HTTPStatus.OK)
async def health_check():
    return

# Use Direct hit mode
@app.get("/direct")
async def treat_request(request: Request):
    return await forward_request(request, manager)

# Use random mode
@app.get("/random")
async def treat_request(request: Request):
    options = [manager] + workers
    mysql_node = random.choice(options)
    return await forward_request(request, mysql_node)

# Use customized mode
@app.get("/customized")
async def treat_request(request: Request):
    return await forward_request_low_latency(request)

# Use Direct hit mode
@app.post("/direct")
async def treat_request(request: Request):
    return await forward_request(request, manager + "/direct")

# Use Random mode (will always write to manager)
@app.post("/random")
async def treat_request(request: Request):
    return await forward_request(request, manager)

# Use Customized mode (will always write to manager)
@app.post("/customized")
async def treat_request(request: Request):
    return await forward_request(request, manager)

async def forward_request(request: Request, address: str):
    # Forward the request to the selected server
    response = await get_response(request, address)

    # Return the response to trusted host
    print(
        f"Received response from {address}: {response.status_code} - {response.content}"
    )
    return {
        "status_code": response.status_code,
        "body": response.json(),
        "headers": dict(response.headers),
    }

async def forward_request_low_latency(request: Request):
    # Get the address with the lowest latency
    response_time, address = heapq.heappop(heap)
    print(f"forward to mysql instance {address} - {response_time}")

    # Forward the request to the selected server
    response = await get_response(request, address)
    heapq.heappush(heap, [response.elapsed, address])
    print(f'{address} took {response.elapsed} to respond')

    # Return the response to trusted host
    print(
        f"Received response from {address}: {response.status_code} - {response.content}"
    )
    return {
        "status_code": response.status_code,
        "body": response.json(),
        "headers": dict(response.headers),
    }

async def get_response(request: Request, address: str): 
    return requests.request(
        method=request.method,
        url=f"http://{address}",
        headers=request.headers,
        data=await request.body(),
        params=request.query_params,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)