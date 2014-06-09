import socket
import sys

PORT = 1888


def run(tcp_ip, tcp_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to", tcp_ip)
    s.connect((tcp_ip, tcp_port))

    s.send(b"3:Hop")
    s.close()

run(sys.argv[1], PORT)
