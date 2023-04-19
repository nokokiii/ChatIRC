import socket
from config import connection, read_data, commands


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(connection)

    run = True
    while run:
        command = input("Enter command: ")
        command += "\r\n\r\n"
        if command.strip('\r\n\r\n') not in commands:
            print("Invalid command")
        elif command == 'QUIT':
            s.sendall(command.encode())
            data = read_data(s)
            data = data.decode()
            data = data.strip('\r\n\r\n')

            print(f'Response from server: {data}')
            s.close()
            run = False
        else:
            s.sendall(command.encode())
            data = read_data(s)
            data = data.decode()
            data = data.strip('\r\n\r\n')

            print(f'Response from server: {data}')

