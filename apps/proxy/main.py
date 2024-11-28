from fastapi import FastAPI, Request
import requests
import uvicorn
from http import HTTPStatus

# Create FastAPI app
app = FastAPI()

@app.get("/health", status_code=HTTPStatus.OK)
async def health_check(request: Request):
    return

@app.get("/")
async def treat_request(request: Request):
    return await treat_message(request)

@app.post("/")
async def treat_request(request: Request):
    return await treat_message(request)

async def treat_message(request: Request):
    message = f"Proxy has received the request"
    return {"message": message}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)