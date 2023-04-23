import socket
from config import connection, read_data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(connection)

    run = True
    while run:
        command = input(f"Enter command:").replace(" ", "").replace("-", " ") + "\r\n\r\n"
        s.sendall(command.encode())

        data = read_data(s)
        data = data.decode()

        print(f'S: {data}')

        if command == f"QUIT\r\n\r\n":
            run = False
