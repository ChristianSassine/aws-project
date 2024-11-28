from time import sleep, time
import requests
from infra import InstanceInfo
from collections import deque

async def isEndpointActive(url):
    try:
        requests.get(f"http://{url}/health")
        return True
    except:
        return False



async def health_check_instances(instances_info):
    # Extract Ips from the instances' info
    instances = deque()
    for info in instances_info:
        instances.append([info[InstanceInfo.ID.value], info[InstanceInfo.PUBLIC_IP.value]])
    
    INTERVALS = 45 # 45s Intervals to check
    TIMEOUT = 60 * 15 # timeout after 15 minutes
    start_time = time()
    print("Checking if the apps are active...")
    while instances:
        sleep(INTERVALS)
        for _ in range(len(instances)):
            instance_id, url = instances.popleft()
            isActive = await isEndpointActive(url)
            if isActive:
                print(f"Instance {instance_id} is ACTIVE!")
                continue
            instances.append([instance_id, url])
            print(f"Instance {instance_id} is not yet ready")
            if time() - start_time > TIMEOUT:
                print("[TIMEOUT]: The instances aren't active after 10 mins")
                return
        print("Retrying...")
    print("All apps are READY!")