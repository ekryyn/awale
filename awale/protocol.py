import json


def extract_msg(data):
    pos = data.find('\n\n')
    message = ''
    if pos > 0:
        expected_len = int(data[:pos])
        msg = data[(pos+2):]
        if len(msg) >= expected_len:
            message, data = msg[:expected_len], msg[expected_len:]
            # some clients may send null terminated strings. Remove it.
            message = message.strip("\x00")
    return message, data


def encode_message(msg_type, msg_val):
    msg = json.dumps({'type': msg_type, 'message': msg_val})
    return "%d\n\n%s" % (len(msg), msg)


def decode_message(msg):
    obj = json.loads(msg)
    return obj['type'], obj['message']


def send(sock, msg_type, msg_val):
    """
    Utility but not really necessary,
    not part of the protocol which is socket independant.
    """
    msg = encode_message(msg_type, msg_val)
    d = "%d\n\n%s" % (len(msg), msg)
    return sock.send(d)


def game_state(game):
    state = {
        'scores': game.scores,
        'game': game.game,
        'to_play': game.current_player,
    }
    return state
