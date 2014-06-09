import socket
import threading


def process_data(message):
    print("received", message)


class AwlServer(threading.Thread):
    IP = '0.0.0.0'
    PORT = 1888

    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind((self.IP, self.PORT))
        self._s.listen(1)

    def run(self):
        print("waiting for client...")
        client, address = self._s.accept()
        print("New client", address)

        running = True
        while running:
            size = ''
            # get size:
            c = None
            while c != ':':
                c = self._s.recv(1)
                if not c:
                    break
                size += c
            size = int(size)
            data = ''
            while len(data) < size:
                d = self._s.recv(1)
                data += d
            # process message
            process_data(data)

        self._s.close()

