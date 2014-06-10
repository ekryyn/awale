import select
import socket
import sys
import time

from protocol import extract_msg

PORT = 1889

try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass


def send(sock, msg):
    d = "%d\n\n%s" % (len(msg), msg)
    sock.send(d)


def run(tcp_ip, tcp_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to", tcp_ip)
    sock.connect((tcp_ip, tcp_port))
#    sock.setblocking(0)
    running = True
    inputs = [sock, sys.stdin]
    data = b''
    while running:
        rds, wts, ers = select.select(inputs, [], [], 1)
        for s in rds:
            if s is sys.stdin:
                cmd = s.readline()
                send(sock, cmd.strip())
            if s is sock:
                d = s.recv(2048)
                if d:
                    data += d
                else:
                    print("lost connection")
                    running = False

        # manage data
        msg, remain = extract_msg(data)
        if msg:
            print(msg)
        data = remain
    sock.close()

if __name__ == "__main__":
    run(sys.argv[1], PORT)
