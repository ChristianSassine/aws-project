import infra
import cleanup
import sys
from constants import *

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "cleanup":
        cleanup.cleanup(KEY_PAIR_NAME, SECURITY_GROUP_NAME)
    elif not args:
        instance = infra.deploy()
