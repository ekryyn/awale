import socket
import select


def process_data(message):
    print("received", message)


class AwlServer(object):
    IP = '0.0.0.0'
    PORT = 1889

    def __init__(self):
        print("Creating server")

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.setblocking(0)
        self._s.bind((self.IP, self.PORT))
        self._s.listen(1)

        self.ins = [self._s]
        self.outs = []
        self.clients = {}

    def run(self):
        print("running...")
        while self.ins:
            rds, wts, ers = select.select(
                self.ins,
                self.outs,
                self.ins,
            )

            for s in rds:
                if s is self._s:
                    if len(self.clients) < 1:
                        cl, addr = s.accept()
                        print("New client %s" % str(addr))
                        self.ins.append(cl)
                        self.clients[cl] = b''
                    else:
                        print("Maximum clients reached")
                        cl, addr = s.accept()
                        cl.close()
                else:
                    data = s.recv(5)
                    if data:
                        self.clients[s] += data
                    else:
                        print("Client disconnected")
                        self.ins.remove(s)
                        self.clients.pop(s)
                        s.close()

            for s in ers:
                print("Error, closing socket.")
                self.ins.remove(s)
                s.close()

            # manage data
            for s in self.clients:
                data = self.clients[s]
                pos = data.find('\n\n')
                if pos > 0:
                    expected_len = int(data[:pos])
                    msg = data[(pos+2):]
                    if len(msg) >= expected_len:
                        # we received all packet, and maybe more
                        msg, data = msg[:expected_len], msg[expected_len:]
                        self.clients[s] = data
                        process_data(msg)

        client.close()
        self._s.close()

