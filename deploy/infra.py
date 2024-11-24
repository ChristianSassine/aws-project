import boto3
import json
import utils
import os
from constants import *


def deploy():
    # Create configs directory
    os.makedirs(utils.get_path(CONFIGS_PATH), exist_ok=True)

    # Create Key/Pair for the EC2 instances
    create_key_pair(KEY_PAIR_NAME)

    # Create Security Group
    grp_id = create_security_group(SECURITY_GROUP_NAME, get_default_ip_permissions())

    # Create instances
    mysql_cluster = create_ec2_instances("t2.micro", 1, KEY_PAIR_NAME, grp_id)

    # Extract instance's information
    cluster_1_info = get_instance_info(mysql_cluster)
    utils.write_file(INSTANCE_INFO_PATH, json.dumps(cluster_1_info))

    return cluster_1_info

def create_key_pair(key_name: str) -> str:
    ec2 = boto3.client("ec2", config=BOTO3_CONFIG)

    key_pair = ec2.create_key_pair(KeyName=key_name)
    # Save the private key to a .pem file
    file_name = f"{CONFIGS_PATH}/{key_name}.pem"
    utils.write_file(file_name, key_pair["KeyMaterial"])

    print(f"Key pair '{key_name}' created and saved to {file_name}.")


def create_security_group(group_name: str, ip_permissions: list):
    ec2 = boto3.client("ec2", config=BOTO3_CONFIG)

    # Create the security group
    response = ec2.create_security_group(
        GroupName=group_name, Description="Security group for the ec2 clusters"
    )
    security_group_id = response["GroupId"]
    print(f"Security Group '{group_name}' created with ID: {security_group_id}")

    # Allow ingress
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=ip_permissions
    )
    print(f"Configured Security Group's '{group_name}' authorizations")

    return security_group_id


def get_default_ip_permissions():
    return [
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0",
                    "Description": "Allow SSH connections from outside",
                }
            ],
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0",
                    "Description": "Allow HTTP connections from outside",
                }
            ],
        },
    ]


def get_secure_ip_permissions(ip_address):
    return [
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [
                {
                    "CidrIp": f"{ip_address}/0",
                    "Description": "Allow HTTP connections from specific ip address",
                }
            ],
        },
    ]


def create_ec2_instances(
    instance_type: str, count: int, key_name: str, sec_group_id: str
):
    # Use resource client
    ec2 = boto3.resource("ec2", config=BOTO3_CONFIG)

    # Create instances
    instances = ec2.create_instances(
        ImageId="ami-0e86e20dae9224db8",  # Ubuntu AMI
        MinCount=count,
        MaxCount=count,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=[sec_group_id],
    )
    print(f"Created {count} EC2 instances of type {instance_type}")

    # Wait for the instances to be running
    for instance in instances:
        instance.wait_until_running()

    return instances


def get_instance_info(instances):
    instances_info = []

    # Refresh instance details
    for instance in instances:
        instance.reload()
        instances_info.append(
            {
                "Instance ID": instance.id,
                "Public IP": instance.public_ip_address,
                "DNS": instance.public_dns_name,
                "Private IP": instance.private_ip_address,
            }
        )

    return instances_info