import sys
import subprocess
from veryfasttree import VFT_BINARY

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        args = ['-ext', 'AUTO']  # Avoid tty message if no arguments

    sys.exit(subprocess.call([VFT_BINARY] + args))
