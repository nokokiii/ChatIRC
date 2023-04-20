import socket
import threading
from datetime import datetime
from config import connection, read_data, generate_id

users = {}

#  Dictionary with channels and messages
channels = {
    '#sports': [],
    '#movies-and-TV-series': [],
    '#games': []
}


#  Dictionary with channels and users
class Channels:
    def __init__(self, name):
        self.name = name if name.startswith('#') else f'#{name}'
        self.chat = []

    def create(self):
        channels[self.name] = []


class Users:
    def __init__(self, name="Guest"):
        self.id = generate_id(len(users))
        self.name = f'{name}#{self.id}'


def user_connect(client_f, addr_f):
    print(f'Connected with {addr_f[0]}')
    while True:
        data = read_data(client_f).decode().strip('\r\n\r\n')
        response = ''

        # HELLO command
        if "HELLO" in data:
            request = data.split('|')

            user = Users(request[1]) if request[1] else Users()
            users[user.id] = user
            response = f'HELLO {user.name}\r\n\r\n'
            client_f.sendall(response.encode())

        # HELP command
        if "HELP" in data:
            response = "COMMANDS: \r\n" \
                "HELLO - to connect to the server\r\n" \
                "LIST - to get list of channels\r\n" \
                "CREATE - to create new channel\r\n" \
                "JOIN - to join channel\r\n" \
                "QUIT - to disconnect from the server\r\n\r\n"
            client_f.sendall(response.encode())

        # QUIT command
        if "QUIT" in data:
            client_f.sendall(f'GOODBYE {user.name}\r\n\r\n'.encode())
            client_f.close()
            break

        # LIST command
        if "LIST" in data:
            response = 'THE LIST OF CHANNELS\r\n'
            # Sending list of channels
            response = ''.join([f' {channel}\r\n' for channel in channels])
            response += '\r\n'

            client_f.sendall(response.encode())

        # CREATE command
        if "CREATE" in data:
            request = data.split('|')
            channel = request[1]
            # Checking if channel already exists
            if channel in channels:
                response = f'CHANNEL {channel} ALREADY EXISTS\r\n\r\n'
            else:
                # Creating new channel
                new_channel = Channels(channel)
                new_channel.create()
                response = f'CHANNEL {channel} CREATED\r\n\r\n'

            client_f.sendall(response.encode())

        # JOIN command
        if "JOIN" in data:
            request = data.split('|')
            channel = request[1]  # Getting channel name

            if channel in channels:  # Checking if channel exists
                response = f'CONNECTED TO {channel}\r\n\r\n'
                client_f.sendall(response.encode())

                while True:
                    data = read_data(client_f).decode().strip('\r\n\r\n')

                    # MESS command
                    if "MESS" in data:
                        request = data.split('|')
                        # Getting current date and time
                        now = datetime.now()  # current date and time
                        short_date = now.strftime("%B")
                        dt_string = now.strftime(f"%d {short_date[:3]} %H:%M:%S")
                        # Creating message text and adding it to the channel
                        channels[channel].append(f'[{dt_string}] {user.name}: {request[1]}')

                        # Sending response to user that message was sent
                        client_f.sendall(f'MESSAGE SENT\r\n\r\n'.encode())

                    # GET command
                    if "GET" in data:
                        # Getting amount of messages to send
                        mess_amount = 10 if len(channels[channel]) > 10 else len(channels[channel])

                        # Creating response
                        client_f.sendall((f'{channel} CHAT (LAST {mess_amount} MESSAGES)\r\n'.join(f'{channels[channel][(len(channels[channel]) - mess_amount) + i]}\r\n' for i in range(mess_amount)) + '\r\n').encode())

                    # QUIT command
                    if "QUIT" in data:
                        client_f.sendall(f'GOODBYE {user.name}\r\n\r\n'.encode())
                        client_f.close()
                        break
            else:
                # Sending response to user if channel doesn't exist
                client_f.sendall('THERE IS NO SUCH A CHANNEL\r\n\r\n'.encode())

    client_f.close()

# Starting server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(connection)
    s.listen(5)
    print(f'Server {connection[0]} started on port: {connection[1]}')
    while True:
        client, addr = s.accept()
        thread = threading.Thread(target=user_connect, args=(client, addr,))
        thread.start()
