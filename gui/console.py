from core import display_game


class Console(object):
    def process_message(self, msg_type, msg_val):
        if msg_type == 'game_state':
            g = display_game(msg_val['game'], msg_val['scores'])
            print(g)
        else:
            print(msg_val)
