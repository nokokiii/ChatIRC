from socket import socket, AF_INET, SOCK_STREAM
from config import connection, read_data


def client(sock: socket) -> None:
    """
    Function for client to send commands to server
    """
    command = (
        input("Enter command:").replace(" ", "").replace("-", " ")
        + "\r\n\r\n"
    )
    sock.sendall(command.encode())

    data = read_data(sock)
    data = data.decode()

    print(f'S: {data}')

    return command != f"QUIT\r\n\r\n"


def main() -> None:
    """
    Run client
    """
    try:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(connection)

            run = True
            while run:
                try:
                    run = client(sock)
                except ConnectionResetError:
                    print("Server stopped working. Try again later.")
                    run = False
    except ConnectionRefusedError:
        print("Server is not running. Try again later.")


if __name__ == "__main__":
    main()
