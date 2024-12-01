import os
import json
from utils import *
from constants import *
from infra import *
from remote import bootstrap_instance, File
from health_check import health_check_instances

async def deploy():
    # Create configs directory
    os.makedirs(get_path(ROOT_CONFIGS_PATH), exist_ok=True)

    # Create Key/Pair for the EC2 instances
    create_key_pair(KEY_PAIR_NAME)
    # TODO: Maybe assign a new key for internal?

    # Deploy Gatekeeper
    ## Create Security Group
    outside_grp_id = create_security_group(
        OUTSIDE_SECURITY_GROUP_NAME, get_outside_ip_permissions()
    )

    ## Create Gatekeeper
    gatekeeper = create_ec2_instances("t2.large", 1, KEY_PAIR_NAME, outside_grp_id)

    ## Extract instance's information
    gatekeeper_info = get_instances_info(gatekeeper)[0]
    write_file(GATEKEEPER_INFO_PATH, json.dumps(gatekeeper_info))

    # Deploy Trusted Host
    ## Create Security Group
    trusted_grp_id = create_security_group(
        TRUSTED_SECURITY_GROUP_NAME, get_outside_ip_permissions()
    )

    ## Create Trusted Host
    trusted_host = create_ec2_instances("t2.large", 1, KEY_PAIR_NAME, trusted_grp_id)

    ## Extract instance's information
    trusted_host_info = get_instances_info(trusted_host)[0]
    write_file(TRUSTED_HOST_INFO_PATH, json.dumps(trusted_host_info))

    # Deploy proxy and clusters
    ## Create Security Group
    internal_grp_id = create_security_group(
        INTERNAL_SECURITY_GROUP_NAME, get_outside_ip_permissions()
    )

    ## Create Proxy
    proxy = create_ec2_instances("t2.large", 1, KEY_PAIR_NAME, internal_grp_id)

    ## Extract instance's information
    proxy_info = get_instances_info(proxy)[0]
    write_file(PROXY_INFO_PATH, json.dumps(proxy_info))

    ## Create Mysql Workers
    mysql_workers = create_ec2_instances("t2.micro", 2, KEY_PAIR_NAME, internal_grp_id)

    ## Extract instances' informations
    mysql_workers_info = get_instances_info(mysql_workers)
    write_file(WORKERS_INFO_PATH, json.dumps(mysql_workers_info))

    print(mysql_workers_info)

    ## Create Mysql Manager
    mysql_manager = create_ec2_instances("t2.micro", 1, KEY_PAIR_NAME, internal_grp_id)
    
    ## Extract instance's informations
    mysql_manager_info = get_instances_info(mysql_manager)[0]
    write_file(MANAGER_INFO_PATH, json.dumps(mysql_manager_info))

    # Bootstrap the instances
    setup_instances(gatekeeper_info, trusted_host_info, proxy_info, mysql_workers_info, mysql_manager_info)

    # Health check to make sure all the servers are active
    instances_info = [gatekeeper_info, trusted_host_info, proxy_info, mysql_manager_info] + mysql_workers_info
    await health_check_instances(instances_info)

    # Modify the security groups to tighten security
    tighten_security_groups(trusted_grp_id, internal_grp_id, gatekeeper_info, proxy_info, trusted_host_info, mysql_manager_info, mysql_workers_info)

def tighten_security_groups(trusted_grp_id, internal_grp_id, gatekeeper_info, proxy_info, trusted_host_info, mysql_manager_info, mysql_workers_info):
    modify_security_group_permissions(
        trusted_grp_id,
        get_secure_ip_permissions(
            [
                gatekeeper_info[InstanceInfo.PRIVATE_IP.value],
                proxy_info[InstanceInfo.PRIVATE_IP.value],
            ]
        ),
    )

    modify_security_group_permissions(
        internal_grp_id,
        get_secure_ip_permissions(
            [
                proxy_info[InstanceInfo.PRIVATE_IP.value],
                trusted_host_info[InstanceInfo.PRIVATE_IP.value],
                mysql_manager_info[InstanceInfo.PRIVATE_IP.value],
            ] + [worker_info[InstanceInfo.PRIVATE_IP.value] for worker_info in mysql_workers_info]
        ),
    )


def setup_instances(gatekeeper_info, trusted_host_info, proxy_info, workers_info, manager_info):
    bootstrap_instance(
        get_path(KEY_PAIR_PATH),
        gatekeeper_info[InstanceInfo.PUBLIC_IP.value],
        [
            File(get_path(APP_BOOTSTRAP_PATH), "bootstrap.sh"),
            File(get_path(GATEKEEPER_APP_PATH), "main.py"),
            File(get_path(TRUSTED_HOST_INFO_PATH), "trusted_host.json"),
        ],
        gatekeeper_info[InstanceInfo.ID.value],
    )

    bootstrap_instance(
        get_path(KEY_PAIR_PATH),
        trusted_host_info[InstanceInfo.PUBLIC_IP.value],
        [
            File(get_path(APP_BOOTSTRAP_PATH), "bootstrap.sh"),
            File(get_path(TRUSTED_HOST_APP_PATH), "main.py"),
            File(get_path(PROXY_INFO_PATH), "proxy.json"),
        ],
        trusted_host_info[InstanceInfo.ID.value],
    )

    bootstrap_instance(
        get_path(KEY_PAIR_PATH),
        proxy_info[InstanceInfo.PUBLIC_IP.value],
        [
            File(get_path(APP_BOOTSTRAP_PATH), "bootstrap.sh"),
            File(get_path(WORKERS_INFO_PATH), "workers.json"),
            File(get_path(MANAGER_INFO_PATH), "manager.json"),
            File(get_path(PROXY_APP_PATH), "main.py"),
        ],
        proxy_info[InstanceInfo.ID.value],
    )

    for worker_info in workers_info:
        bootstrap_instance(
            get_path(KEY_PAIR_PATH),
            worker_info[InstanceInfo.PUBLIC_IP.value],
            [
                File(get_path(MYSQL_BOOTSTRAP_PATH), "bootstrap.sh"),
                File(get_path(MYSQL_WORKER_MAIN_PATH), "main.py"),
                File(get_path(MYSQL_DEP_PATH), "db.py"),
            ],
            worker_info[InstanceInfo.ID.value],
        )
    
    bootstrap_instance(
            get_path(KEY_PAIR_PATH),
            manager_info[InstanceInfo.PUBLIC_IP.value],
            [
                File(get_path(MYSQL_BOOTSTRAP_PATH), "bootstrap.sh"),
                File(get_path(MYSQL_MANAGER_MAIN_PATH), "main.py"),
                File(get_path(MYSQL_DEP_PATH), "db.py"),
                File(get_path(WORKERS_INFO_PATH), "workers.json"),
            ],
            manager_info[InstanceInfo.ID.value],
        )