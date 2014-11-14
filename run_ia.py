import sys
from awale import client
from awale.random_ai import RandomAI
from awale.gui.console import Console

if __name__ == '__main__':
    if len(sys.argv) > 1:
        computer_player = RandomAI()
        gui = Console()
        client.run(sys.argv[1], client.PORT, gui, computer_player)
    else:
        print("Please provide a server address to connect to")

