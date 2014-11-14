import sys
from .. import protocol

if __name__ == '__main__':
    running = True
    data = ''
    while running:
        data += sys.stdin.read(2048)
        if data:
            print("received %s" % data)
            data = ''

