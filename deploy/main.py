import launch
from cleanup import cleanup
import sys
from constants import *
import asyncio

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "cleanup":
        cleanup()
    elif not args:
        asyncio.run(launch.deploy())
