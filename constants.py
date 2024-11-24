from botocore.config import Config

# Configurations
CONFIGS_PATH = "configs"
KEY_PAIR_NAME = "CLOUD"
SECURITY_GROUP_NAME = "deploy_group"
INSTANCE_INFO_PATH = CONFIGS_PATH + "/instance_info.json"

# Scripts
SCRIPTS = "scripts"

# BOTO3 Configs
REGION = "us-east-1"
BOTO3_CONFIG = Config(region_name=REGION)
 
