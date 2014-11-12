import select
import socket
import sys
import time

from protocol import extract_msg, send, decode_message

PORT = 1889

try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass


def run(tcp_ip, tcp_port, gui, ai=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to", tcp_ip)
    sock.connect((tcp_ip, tcp_port))
#    sock.setblocking(0)
    running = True
    inputs = [sock,]
    if ai is None:
        inputs.append(sys.stdin)

    data = b''
    while running:
        rds, wts, ers = select.select(inputs, [], [], 0)
        for s in rds:
            if s is sys.stdin:
                cmd = s.readline()
                send(sock, 'play', cmd.strip())
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
            mtype, mval = decode_message(msg)
            gui.process_message(mtype, mval)

            # if an AI is attached, ask for a play
            if ai is not None:
                play = ai.process_message(mtype, mval)
                if play is not None:
                    send(sock, 'play', play)
        data = remain
    sock.close()

if __name__ == "__main__":
    run(sys.argv[1], PORT)
