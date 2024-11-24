from fastapi import FastAPI, Request
import requests
import uvicorn

# Create FastAPI app
app = FastAPI()


@app.get("/")
async def send_trusted_host_get(request: Request):
    return await treat_message(request)

@app.post("/")
async def send_trusted_host_get(request: Request):
    return await treat_message(request)

async def treat_message(request: Request):
    message = f"Trusted host has received the request"
    return {"message": message}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)