from fastapi import FastAPI, Request
import requests
import uvicorn
import json
from http import HTTPStatus

# Create FastAPI app
app = FastAPI()

with open("trusted_host.json", "r") as f:
    trusted_host_data = json.load(f)
    trusted_host_ip = trusted_host_data["Private IP"]

@app.get("/health", status_code=HTTPStatus.OK)
async def health_check(request: Request):
    return

@app.get("/")
async def send_trusted_host_get(request: Request):
    return await treat_message(request)


@app.post("/")
async def send_trusted_host_post(request: Request):
    return await treat_message(request)

async def treat_message(request: Request):
    # Get the instance with the smallest response time
    print(f"Received message")

    # Forward the request to the selected server
    response = requests.request(
        method=request.method,
        url=f"http://{trusted_host_ip}",
        headers=request.headers,
        data=await request.body(),
        params=request.query_params,
    )

    # Return the response from the backend server
    print(
        f"Received response from {trusted_host_ip}: {response.status_code} - {response.content}"
    )
    return {
        "status_code": response.status_code,
        "body": response.json(),
        "headers": dict(response.headers),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
