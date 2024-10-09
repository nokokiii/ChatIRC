from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from src.config import connection
from src.server.utils.server import Server


def run_server() -> None:
    """
    Main function for running whole server
    """
    server = Server(connection=connection)

    with socket.socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(connection)
        sock.listen(5)
        print(f'Server {connection[0]} started on port: {connection[1]}')

        while True:
            client, addr = sock.accept()
            thread = Thread(target=server.handle_new_user, args=(client, addr,))
            thread.start()


if __name__ == '__main__':
    run_server()
