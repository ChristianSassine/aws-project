import boto3
import utils
from constants import *
from enum import Enum


def create_key_pair(key_name: str) -> str:
    ec2 = boto3.client("ec2", config=BOTO3_CONFIG)

    key_pair = ec2.create_key_pair(KeyName=key_name)
    # Save the private key to a .pem file
    file_name = f"{ROOT_CONFIGS_PATH}{key_name}.pem"
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
        GroupId=security_group_id, IpPermissions=ip_permissions
    )
    print(f"Configured Security Group's '{group_name}' authorizations")

    return security_group_id


def modify_security_group_permissions(group_id: str, ip_permissions: list):
    ec2 = boto3.client("ec2", config=BOTO3_CONFIG)

    # Get current rules
    response = ec2.describe_security_groups(GroupIds=[group_id])
    current_rules_ingress = response["SecurityGroups"][0]["IpPermissions"]
    current_rules_egress = response["SecurityGroups"][0]["IpPermissionsEgress"]

    # Revoke rules
    ec2.revoke_security_group_ingress(GroupId=group_id, IpPermissions=current_rules_ingress)
    ec2.revoke_security_group_egress(GroupId=group_id, IpPermissions=current_rules_egress)

    print(f"Security Group's '{group_id}' authorizations have been removed")

    # Allow ingress
    ec2.authorize_security_group_ingress(GroupId=group_id, IpPermissions=ip_permissions)
    # Allow egress
    ec2.authorize_security_group_egress(GroupId=group_id, IpPermissions=ip_permissions)
    print(f"Configured Security Group's '{group_id}' authorizations")

    return


def get_outside_ip_permissions():
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

def get_secure_ip_permissions_with_ssh(ip_addresses: list):
    return [
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [
                {
                    "CidrIp": f"{ip_address}/32",
                    "Description": "Allow SSH connections from specific ip address",
                }
                for ip_address in ip_addresses
            ],
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [
                {
                    "CidrIp": f"{ip_address}/32",
                    "Description": "Allow HTTP connections from specific ip address",
                }
                for ip_address in ip_addresses
            ],
        },
    ]

def get_secure_ip_permissions(ip_addresses: list):
    return [
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [
                {
                    "CidrIp": f"{ip_address}/32",
                    "Description": "Allow HTTP connections from specific ip address",
                }
                for ip_address in ip_addresses
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


class InstanceInfo(Enum):
    ID = "INSTANCE ID"
    PUBLIC_IP = "Public IP"
    DNS = "DNS"
    PRIVATE_IP = "Private IP"

def get_instances_info(instances):
    instances_info = []

    # Refresh instance details
    for instance in instances:
        instance.reload()
        instances_info.append(
            {
                InstanceInfo.ID.value: instance.id,
                InstanceInfo.PUBLIC_IP.value: instance.public_ip_address,
                InstanceInfo.DNS.value: instance.public_dns_name,
                InstanceInfo.PRIVATE_IP.value: instance.private_ip_address,
            }
        )

    return instances_info
