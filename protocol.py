import json


def extract_msg(data):
    pos = data.find('\n\n')
    message = ''
    if pos > 0:
        expected_len = int(data[:pos])
        msg = data[(pos+2):]
        if len(msg) >= expected_len:
            message, data = msg[:expected_len], msg[expected_len:]
            # some clients may send null terminated strings.
            # we'll then end up with a "ramaining" containing a NULL char
            # at the beginning
            data = data.strip("\x00")
    return message, data


def send(sock, msg_type, msg_val):
    msg = json.dumps({'type': msg_type, 'message': msg_val})
    d = "%d\n\n%s" % (len(msg), msg)
    return sock.send(d)


def decode_message(msg):
    obj = json.loads(msg)
    return obj['type'], obj['message']
