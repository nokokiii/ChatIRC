import socket
from config import connection, read_data

size = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(connection)

    # Hello request ✓
    request = "HELLO|KUBA\r\n\r\n"
    # print(request)
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # List request
    request = "LIST\r\n\r\n"
    # print(request)
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # Create request
    req_channel = "#games"
    request = f"CREATE|{req_channel}\r\n\r\n"
    # print(request)
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # List request
    request = "LIST\r\n\r\n"
    # print(request)
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    # Join request
    request = f"JOIN|{req_channel}\r\n\r\n"
    # print(request)
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()

    print(f'Response from server: {data}')

    if "CONNECTED TO" in data:
        message = "Hello"
        request = f"MESS|{message}\r\n\r\n"
        # print(request)
        s.sendall(request.encode())

        data = read_data(s)
        data = data.decode()
        print(f'Response from server: {data}')

        request = "GETMESS\r\n\r\n"
        # print(request)
        s.sendall(request.encode())

        data = read_data(s)
        data = data.decode()

        print(f'Response from server: {data}')
    else:
        print(f"There is no such a channel {req_channel}")

    # Quit request
    request = "QUIT\r\n\r\n"
    # print(request)
    s.sendall(request.encode())

    data = read_data(s)
    data = data.decode()
    print(f'Response from server: {data}')

    s.close()