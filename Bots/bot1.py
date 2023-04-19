import socket
from config import connection, read_data

size = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(connection)

    # Hello request ✓
    request = "HELLO\r\nKUBA\r\n\r\n"
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # List request
    request = "LIST\r\n\r\n"
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # Create request
    req_channel = "#games"
    request = f"CREATE\r\n{req_channel}\r\n\r\n"
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # List request
    request = "LIST\r\n\r\n"
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # Join request
    request = f"JOIN\r\n{req_channel}\r\n\r\n"
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()

    print(f'Response from server: {data}')

    if "CONNECTED TO" in data:
        print(f"You successfully joined the {req_channel} channel")
        message = "Hello"
        request = f"MESS\r\n{message}\r\n\r\n"
        s.sendall(request.encode())

        data = read_data(s)
        data = data.decode()

        print(f'Response from server: {data}')

        request = "GET\r\n\r\n"
        s.sendall(request.encode())

        data = read_data(s)
        data = data.decode()

        print(f'Response from server: {data}')
    else:
        print(f"There is no such a channel {req_channel}")

    s.close()