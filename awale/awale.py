import sys
from server import AwlServer
import client
from gui.console import Console


def create_server():
    s = AwlServer()
    return s

if __name__ == '__main__':
    gui = Console()
    if len(sys.argv) > 1:
        client.run(sys.argv[1], client.PORT, gui)
    else:
        s = create_server()
        try:
            s.start()
            client.run('127.0.0.1', client.PORT, gui)
        except KeyboardInterrupt:
            print("Shutting down...")
            s.running = False
            s.join()

