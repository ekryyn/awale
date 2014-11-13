from server import AwlServer
from gui.console import Console
import time


def create_server():
    s = AwlServer()
    s.daemon = True
    return s

if __name__ == '__main__':
    gui = Console()
    s = create_server()
    try:
        s.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Shutting down...")
        s.running = False
        s.join()

