import sys
from server import AwlServer


def create_server():
    s = AwlServer()
    s.run()
    return s

if __name__ == '__main__':
    s = create_server()
