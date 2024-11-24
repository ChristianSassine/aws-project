import os
import json
import utils
from constants import *
from infra import *

def deploy():
    # Create configs directory
    os.makedirs(utils.get_path(CONFIGS_PATH), exist_ok=True)
    
    # Create Key/Pair for the EC2 instances
    create_key_pair(KEY_PAIR_NAME)

    # Deploy the Gatekeeper and trusted host
    deploy_gatekeeper()

    # Deploy the Proxy
    #
    # TODO

    # Deploy the cluster
    # TODO


def deploy_gatekeeper():
    # Deploy Gatekeeper
    ## Create Security Group
    default_grp_id = create_security_group(DEFAULT_SECURITY_GROUP_NAME, get_default_ip_permissions())

    ## Create Gatekeeper
    gatekeeper = create_ec2_instances("t2.micro", 1, KEY_PAIR_NAME, default_grp_id)

    ## Extract instance's information
    gatekeeper_info = get_instance_info(gatekeeper)
    utils.write_file(GATEKEEPER_INFO_PATH, json.dumps(gatekeeper_info))

    # Deploy Trusted Host
    # TODO: Add IPs of Proxy and Gatekeeper => Gatekeeper <-> Trusted Host <-> Proxy
    ## Create Secure Security Group
    secure_grp_id = create_security_group(PRIVATE_SECURITY_GROUP_NAME, get_secure_ip_permissions(["0.0.0.0"]))
    
    ## Create Trusted Host
    trusted_host = create_ec2_instances("t2.micro", 1, KEY_PAIR_NAME, secure_grp_id)

    ## Extract instance's information
    trusted_host_info = get_instance_info(trusted_host)
    utils.write_file(TRUSTED_HOST_PATH, json.dumps(trusted_host_info))
    