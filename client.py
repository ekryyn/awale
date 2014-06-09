import socket
import sys
import time

PORT = 1889


def run(tcp_ip, tcp_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to", tcp_ip)
    s.connect((tcp_ip, tcp_port))

    s.send(b"3\n\nHop2\n\nYo")
    s.send(b"7\n\nBonjour6\n\nFreddy")

    time.sleep(3)
    s.close()

run(sys.argv[1], PORT)
