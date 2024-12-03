from botocore.config import Config

# Configurations
### Names
KEY_PAIR_NAME = "CLOUD"
OUTSIDE_SECURITY_GROUP_NAME = "default_group"
TRUSTED_SECURITY_GROUP_NAME = "trusted_group"
INTERNAL_SECURITY_GROUP_NAME = "internal_group"
APP_SCRIPT_NAME = "bootstrap_app"
MYSQL_SCRIPT_NAME = "bootstrap_mysql"
IPTABLES_CONFIG_NAME = "configure_iptables"
IP_ENV = "IP_ADDR"

### Paths
# INSTANCES INFOS
ROOT_CONFIGS_PATH = "configs/"
KEY_PAIR_PATH = ROOT_CONFIGS_PATH + KEY_PAIR_NAME + ".pem"
GATEKEEPER_INFO_PATH = ROOT_CONFIGS_PATH + "gatekeeper_info.json"
TRUSTED_HOST_INFO_PATH = ROOT_CONFIGS_PATH + "trusted_host_info.json"
PROXY_INFO_PATH = ROOT_CONFIGS_PATH + "proxy_info.json"
WORKERS_INFO_PATH = ROOT_CONFIGS_PATH + "workers_info.json"
MANAGER_INFO_PATH = ROOT_CONFIGS_PATH + "manager_info.json"

# Apps
GATEKEEPER_APP_PATH = "../apps/gatekeeper/main.py"
TRUSTED_HOST_APP_PATH = "../apps/trusted_host/main.py"
PROXY_APP_PATH = "../apps/proxy/main.py"
MYSQL_APP_PATH = "../apps/mysql_cluster/"
MYSQL_MANAGER_MAIN_PATH = MYSQL_APP_PATH + "manager.py"
MYSQL_WORKER_MAIN_PATH = MYSQL_APP_PATH + "worker.py"
MYSQL_DEP_PATH = "../apps/mysql_cluster/db.py"

# Scripts
SCRIPTS_PATH = "scripts/"
APP_BOOTSTRAP_PATH = SCRIPTS_PATH + APP_SCRIPT_NAME + ".sh"
MYSQL_BOOTSTRAP_PATH = SCRIPTS_PATH + MYSQL_SCRIPT_NAME + ".sh"
IPTABLES_CONFIG_PATH = SCRIPTS_PATH + IPTABLES_CONFIG_NAME + ".sh"

# BOTO3 Configs
REGION = "us-east-1"
BOTO3_CONFIG = Config(region_name=REGION)
 
