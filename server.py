import socket
import threading


def process_data(message):
    print("received", message)


class AwlServer(threading.Thread):
    IP = '0.0.0.0'
    PORT = 1889

    def __init__(self):
        super(AwlServer, self).__init__()
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind((self.IP, self.PORT))
        self._s.listen(1)

    def run(self):
        print("waiting for client...")
        client, address = self._s.accept()
        print("New client", address)

        running = True
        data = ''
        while running:
            while '\n\n' not in data:
                rec = client.recv(5)
                data = data + rec
            pos = data.find('\n\n')
            expected_len = int(data[:pos])
            msg = data[(pos+2):]
            cur_len = len(msg)
            while cur_len < expected_len:
                msg += str(client.recv(5))
                cur_len = len(msg)

            # if received more than 1, keep our part
            msg, data = msg[:expected_len], msg[expected_len:]
            print("received:", msg)

        client.close()
        self._s.close()

