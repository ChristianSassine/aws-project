from fastapi import FastAPI, Request
import requests
import uvicorn

# Create FastAPI app
app = FastAPI()

TRUSTED_HOST = ""

@app.get("/")
async def send_trusted_host_get(request: Request):
    return treat_message(request)

@app.post("/")
async def send_trusted_host_get(request: Request):
    return treat_message(request)

async def treat_message(request: Request):
    # Get the instance with the smallest response time
    print(f"Received message")

    # Forward the request to the selected server
    response = requests.request(
        method=request.method,
        url=f"http://{TRUSTED_HOST}",
        headers=request.headers,
        data=await request.body(),
        params=request.query_params,
    )
    
    # Return the response from the backend server
    print(
        f"Received response from {TRUSTED_HOST}: {response.status_code} - {response.content}"
    )
    return {
        "status_code": response.status_code,
        "body": response.json(),
        "headers": dict(response.headers)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)