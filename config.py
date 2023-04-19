ip = 'localhost'
port = 56790
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


#
# # Funkcja do wysyłania wiadomości do wszystkich użytkowników w danym kanale
# def broadcast(channel, message):
#     for user in channels[channel]:
#         user.sendall(message.encode('utf-8'))