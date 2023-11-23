import socket
from config import connection, read_data

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(connection)

        run = True
        while run:
            try:
                command = (
                    input("Enter command:").replace(" ", "").replace("-", " ")
                    + "\r\n\r\n"
                )
                s.sendall(command.encode())

                data = read_data(s)
                data = data.decode()

                print(f'S: {data}')

                if command == f"QUIT\r\n\r\n":
                    run = False
            except ConnectionResetError:
                print("Server stopped working. Try again later.")
                run = False
except ConnectionRefusedError:
    print("Server is not running. Try again later.")
