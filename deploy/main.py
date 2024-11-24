import launch
from cleanup import cleanup
import sys
from constants import *

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "cleanup":
        cleanup()
    elif not args:
        instance = launch.deploy()
