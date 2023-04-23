ip = 'localhost'
port = 56990
connection = (ip, port)
commands = ['HELLO', 'JOIN', 'LIST', 'MESS', 'QUIT', 'HELP']


def read_data(socket):
    data = b''
    while b'\r\n\r\n' not in data:
        data += socket.recv(1)

    return data


def generate_id(counter):
    generated_id = hex(counter)[2:].zfill(2)
    counter += 1
    return generated_id


class TextColors:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    yellow = "\u001b[0;33m"
    blue = "\u001b[0;34m"
    magenta = "\u001b[0;35m"
    cyan = '\u001b [0; 36m'
    white = "\u001b[0;37m"
    underline = "\u001b[4m"
    bold = "\u001b[1m"
    inverse = "\u001b[7m"
    end = "\u001b[0m"
