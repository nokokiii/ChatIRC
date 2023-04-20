import socket
from config import connection, read_data, commands


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(connection)

    run = True
    while run:
        command = input("Enter command: ").replace(" ", "") + "\r\n\r\n"
        s.sendall(command.encode())

        data = read_data(s)
        data = data.decode()

        print(f'Response from server: {data}')

        if command == "QUIT\r\n\r\n":
            run = False
