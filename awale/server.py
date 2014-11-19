import socket
import select
import threading

from protocol import extract_msg, send, decode_message
from core import GameState, AwaleException, game_over, winner


def process_data(message):
    print("received", message)


def player_name(no):
    return "Player %d" % (no + 1)


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

    def broadcast(self, msg_type, msg_val):
        for c in self.clients:
            send(c, msg_type, msg_val)

    def send_game(self, client=None):
        state = {
            'scores': self.game.scores,
            'game': self.game.game,
            'to_play': self.game.current_player,
        }
        if client:
            send(client, 'game_state', state)
        else:
            self.broadcast('game_state', state)

    def process_msg(self, client, msg):
        if len(self.players) != 2:
            send(client, 'info', "Waiting for opponent")
            return
        msg_type, msg = decode_message(msg)

        if msg_type == 'play':
            try:
                self.game.play(self.players[client], msg)
                p = player_name(self.players[client])
                self.broadcast('info', "%s played %s" % (p, msg))
                self.send_game()
            except AwaleException as e:
                send(client, 'error', str(e))
            if self.game.over():
                win_player = winner(self.game.game, self.game.scores)
                if win_player is not None:
                    self.broadcast(
                        'info',
                        "%s wins !" % player_name(win_player)
                    )
                else:
                    self.broadcast(
                        'info',
                        "Draw !"
                    )
                self.running = False

    def run(self):
        print("running...")
        self.running = True
        while self.running and self.ins:
            rds, wts, ers = select.select(
                self.ins,
                self.outs,
                self.ins,
                0
            )

            for s in rds:
                if s is self._s:
                    if len(self.clients) < 2:
                        cl, addr = s.accept()
                        print("New client %s" % str(addr))
                        self.ins.append(cl)
                        self.clients[cl] = b''
                        player_no = len(self.players)
                        pname = player_name(player_no)
                        send(cl, 'info', "welcome %s" % pname)
                        send(cl, 'player_id', player_no)
                        self.players[cl] = player_no

                        if len(self.players) == 2:
                            self.broadcast('info', "Ready to play")
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
                                'info',
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

