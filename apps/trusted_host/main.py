from fastapi import FastAPI, Request
import requests
import uvicorn
from http import HTTPStatus
import json

# Create FastAPI app
app = FastAPI()

with open("proxy.json", "r") as f:
    proxy_data = json.load(f)
    proxy = proxy_data["Private IP"]

@app.get("/health", status_code=HTTPStatus.OK)
async def health_check(request: Request):
    return

@app.get("/")
async def redirect_to_proxy(request: Request):
    return await treat_message(request)


@app.post("/")
async def redirect_to_proxy(request: Request):
    return await treat_message(request)

async def treat_message(request: Request):
    print(f"Received message")

    # Forward the request to the selected server
    response = requests.request(
        method=request.method,
        url=f"http://{proxy}",
        headers=request.headers,
        data=await request.body(),
        params=request.query_params,
    )

    # Return the response to trusted host
    print(
        f"Received response from {proxy}: {response.status_code} - {response.content}"
    )
    return {
        "status_code": response.status_code,
        "body": response.json(),
        "headers": dict(response.headers),
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)