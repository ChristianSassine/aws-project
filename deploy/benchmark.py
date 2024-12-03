import asyncio
import aiohttp
import json
import time
from utils import *
from constants import *

async def call_endpoint_http_get(session: aiohttp.ClientSession, request_num, mode, gatekeeper_address):

    url = f"http://{gatekeeper_address}/{mode}"  # Replace with your actual load balancer URL
    headers = {'content-type': 'application/json'}
    
    try:
        async with session.get(url, headers=headers) as response:
            status_code = response.status
            response_json = await response.json()
            print(f"Request {request_num}: Status Code: {status_code}")
            return status_code, response_json
    except Exception as e:
        print(f"Request {request_num}: Failed - {str(e)}")
        return None, str(e)
    
async def call_endpoint_http_post(session: aiohttp.ClientSession, request_num, mode, gatekeeper_address):

    url = f"http://{gatekeeper_address}/{mode}"  # Replace with your actual load balancer URL
    headers = {'content-type': 'application/json'}
    
    try:
        async with session.post(url, headers=headers, json={"first_name":"John", "last_name": "Project"}) as response:
            status_code = response.status
            response_json = await response.json()
            print(f"Request {request_num}: Status Code: {status_code}")
            return status_code, response_json
    except Exception as e:
        print(f"Request {request_num}: Failed - {str(e)}")
        return None, str(e)

async def launch_requests():
    with open(get_path(GATEKEEPER_INFO_PATH), 'r') as f:
        gatekeeper_data = json.load(f)
        gatekeeper_address = gatekeeper_data["DNS"]

    print("Beginning benchmarking...")
    num_requests = 1000
    
    modes = ["direct", "random", "customized"]

    INTERVAL = 5    # Timeout for 5 seconds for better readability
    for mode in modes:
        time.sleep(INTERVAL)
        start_time = time.time()
        print(f"Launching requests for {mode} mode")
        async with aiohttp.ClientSession() as session:
            print("Starting READ requests...")
            tasks = [call_endpoint_http_get(session, i, mode, gatekeeper_address) for i in range(num_requests)]
            await asyncio.gather(*tasks)
        async with aiohttp.ClientSession() as session:
            print("Starting WRITE requests...")
            tasks = [call_endpoint_http_post(session, i, mode, gatekeeper_address) for i in range(num_requests)]
            await asyncio.gather(*tasks)
        end_time = time.time()
        print(f"\nTotal time taken: {end_time - start_time:.2f} seconds")
        print(f"Average time per request: {(end_time - start_time) / num_requests:.4f} seconds")