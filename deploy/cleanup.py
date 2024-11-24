import boto3
from utils import get_path
from shutil import rmtree
from constants import *


def cleanup(key_name, sec_group_name):
    terminate_all_instances()
    delete_key(key_name)
    delete_security_group(sec_group_name)


def delete_key(keyName):
    ec2 = boto3.client("ec2", config=BOTO3_CONFIG)
    ec2.delete_key_pair(KeyName=keyName)
    print(f"Deleted key {keyName}")


def delete_security_group(group_name):
    ec2 = boto3.client("ec2", config=BOTO3_CONFIG)
    ec2.delete_security_group(GroupName=group_name)
    print(f"Deleted security group {group_name}")


def delete_misc_files():
    path = get_path(CONFIGS_PATH)
    rmtree(path)
    print(f"Deleted configuration files")


def terminate_all_instances():
    # Create an EC2 client
    ec2 = boto3.client("ec2", config=BOTO3_CONFIG)

    # Get information about all instances
    response = ec2.describe_instances()

    # Collect all instance IDs
    instance_ids = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])

    if instance_ids:
        # Terminate all instances
        print(f"Terminating instances: {instance_ids}")
        ec2.terminate_instances(InstanceIds=instance_ids)
        print("Termination in progress...")
        waiter = ec2.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=instance_ids)
        print("Instances termination done")
        delete_misc_files()
    else:
        print("No instances to terminate.")
