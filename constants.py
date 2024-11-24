from botocore.config import Config

# Configurations
### Names
CONFIGS_PATH = "configs"
KEY_PAIR_NAME = "CLOUD"
DEFAULT_SECURITY_GROUP_NAME = "default_group"
PRIVATE_SECURITY_GROUP_NAME = "private_group"
### Paths
GATEKEEPER_INFO_PATH = CONFIGS_PATH + "/gatekeeper_info.json"
TRUSTED_HOST_PATH = CONFIGS_PATH + "/trusted_host_info.json"
INSTANCE_INFO_PATH = CONFIGS_PATH + "/instance_info.json"

# Scripts
SCRIPTS = "scripts"

# BOTO3 Configs
REGION = "us-east-1"
BOTO3_CONFIG = Config(region_name=REGION)
 
