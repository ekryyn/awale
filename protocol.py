def extract_msg(data):
    pos = data.find('\n\n')
    message= ''
    if pos > 0:
        expected_len = int(data[:pos])
        msg = data[(pos+2):]
        if len(msg) >= expected_len:
            message, data = msg[:expected_len], msg[expected_len:]
    return message, data

def send(sock, msg):
    d = "%d\n\n%s" % (len(msg), msg)
    return sock.send(d)
