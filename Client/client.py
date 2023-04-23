import socket
from config import connection, read_data, commands, TextColors
C = TextColors


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(connection)

    run = True
    while run:
        command = input(f"{C.magenta}{C.bold}Enter command:{C.end}").replace(" ", "").replace("-", " ") + "\r\n\r\n"
        s.sendall(command.encode())

        data = read_data(s)
        data = data.decode()

        print(f'{C.bold}Response from server: {C.end}{C.bold}{data}')

        if command == f"QUIT\r\n\r\n":
            run = False
