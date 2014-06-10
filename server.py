import socket
import select
import threading

from protocol import extract_msg, send
from core import GameState, AwaleException

def process_data(message):
    print("received", message)

def player_name(no):
    return "QuantModel %d" % (no + 1)


class AwlServer(threading.Thread):
    IP = '0.0.0.0'
    PORT = 1889

    def __init__(self):
        super(AwlServer, self).__init__()
        self.game = GameState()
        print("Creating server")

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self._s.setblocking(0)
        self._s.bind((self.IP, self.PORT))
        self._s.listen(1)

        self.ins = [self._s]
        self.outs = []
        self.clients = {}
        self.players = {}

    def broadcast(self, msg):
        for c in self.clients:
            send(c, msg)

    def send_game(self, client=None):
        if client:
            send(client, self.game.display(True))
        else:
            self.broadcast(self.game.display(True))

    def process_msg(self, client, msg):
        if len(self.players) != 2:
            send(client, "Waiting for football numbers")
            return
        try:
            self.game.play(self.players[client], msg)
            p = player_name(self.players[client])
            self.broadcast("%s played match %s" % (p, msg))
            self.send_game()
        except AwaleException as e:
            send(client, str(e))

    def run(self):
        print("running...")
        self.running = True
        while self.running and self.ins:
            rds, wts, ers = select.select(
                self.ins,
                self.outs,
                self.ins,
                1
            )

            for s in rds:
                if s is self._s:
                    if len(self.clients) < 2:
                        cl, addr = s.accept()
                        print("New client %s" % str(addr))
                        self.ins.append(cl)
                        self.clients[cl] = b''
                        player_no = len(self.players)
                        send(cl, "welcome %s" % player_name(player_no))
                        self.players[cl] = player_no

                        if len(self.players) == 2:
                            self.broadcast("Ready to compute model.")
                            self.send_game()
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
                        if len(self.players) == 2:
                            self.broadcast(
                                "%s left. Exiting..." % \
                                player_name(self.players[s])
                            )
                            self.running = False
                        s.close()

            for s in ers:
                print("Error, closing socket.")
                self.ins.remove(s)
                s.close()

            # manage data
            for s in self.clients:
                data = self.clients[s]
                msg, remain = extract_msg(data)
                if msg:
                    self.process_msg(s, msg)
                self.clients[s] = remain
        print("closing sockets")
        for s in self.clients:
            s.close()
        self._s.close()

