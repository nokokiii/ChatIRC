import socket
import threading
from datetime import datetime

from config import connection, read_data, generate_id, \
    Errors, Themes, commands_help, theme_command, themelist_command, join_command
from src.server.utils.themes import Themes

ERRORS = Errors()
THEME = Themes()

# Dictionary with users
users = {}

#  Dictionary with channels and their data
channels = {}

class Channels:
    def __init__(self, name, password, max_users):
        self.name = name if name.startswith('#') else f'#{name}'
        self.password = password
        self.isLocked = True if password else False
        self.max_users = max_users
        self.users = []
        self.chat = []

    def create(self):
        channels[self.name] = self


class Users:
    def __init__(self, name="Guest"):
        self.id = generate_id(len(users))
        self.name = f'{name}#{self.id}'


def user_connect(client_f, addr_f):
    print(f'Connected with {addr_f[0]}')
    while True:
        data = read_data(client_f).decode().strip('\r\n\r\n')
        request = data.split('|')

        # HELLO command {HELLO|<name>}
        if request[0].upper() == "HELLO":
            if len(request) == 2:
                user = Users(request[1]) if request[1] else Users()
                users[user.id] = user
                response = f'{THEME.response}HELLO {user.name}{THEME.end}\r\n\r\n'
                client_f.sendall(response.encode())

                while True:
                    data = read_data(client_f).decode().strip('\r\n\r\n')
                    request = data.split('|')

                    # HELLO command {HELLO|<name>}
                    if request[0].upper() == "HELLO":
                        client_f.sendall(f'{ERRORS.er_msg("3")}\r\n\r\n'.encode())

                    elif request[0].upper() == "THEME":
                        theme_command(THEME, ERRORS, client_f, request)

                    elif request[0].upper() == "THEMELIST":
                        if len(request) == 1:
                            themelist_command(THEME, client_f)
                        else:
                            client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())

                    elif request[0].upper() == "HELP":
                        if len(request) == 1:
                            client_f.sendall(f'{THEME.response}{commands_help}{THEME.end}\r\n\r\n'.encode())
                        else:
                            client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())

                    # LIST command {LIST}
                    elif request[0].upper() == "LIST":
                        if len(request) == 1:
                            response = 'The list of channels\r\n'
                            for channel in channels:
                                privacy = 'Private' if channels[channel].isLocked else 'Public'
                                response += f'{channel} [{len(channels[channel].users)}/{channels[channel].max_users}] {privacy}\r\n'
                            response += f'{THEME.end}\r\n\r\n'
                            client_f.sendall(response.encode())
                        else:
                            client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())

                    # CREATE command {CREATE|<channel_name>|<password>|<max_users>}
                    elif request[0].upper() == "CREATE":
                        if len(request) == 1 or len(request) > 4 or request[1] == "" or len(request) == 4 and not request[3].isdigit() or len(request) == 3 and request[2] == "" or len(request) == 4 and request[3].isdigit() or len(request) == 3 and request[2] != 0:
                            client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())
                        else:
                            channel = str(request[1]).replace(" ", "")
                            password = str(request[2]) if len(request) >= 3 else None
                            max_users = int(request[3]) if len(request) == 4 else 10
                            # Checking if channel already exists
                            if f'#{channel}' in channels:
                                response = f'{ERRORS.er_msg("9")}\r\n\r\n'
                            else:
                                # Creating new channel
                                new_channel = Channels(channel, password, max_users)
                                new_channel.create()
                                response = f'{THEME.response}Channel {channel} created{THEME.end}\r\n\r\n'

                            client_f.sendall(response.encode())

                    # JOIN command {JOIN|<channel>|<password>}
                    elif request[0].upper() == "JOIN":
                        join_command(client_f, request, user, channels, ERRORS, THEME, datetime)

                    # Sending error if user try to use GET or MESS command while not being connected to channel
                    elif request[0].upper() in ["GET", "MESS", "LEAVE"]:
                        client_f.sendall(f'{ERRORS.er_msg("4")}\r\n\r\n'.encode())

                    # Invalid command
                    else:
                        client_f.sendall(f'{ERRORS.er_msg("0")}\r\n\r\n'.encode())
            else:
                # Sending error if user doesn't provide username
                client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())

        # HELP command
        elif request[0].upper() == "HELP":
            if len(request) == 1:
                client_f.sendall(f'{THEME.response}{commands_help}{THEME.end}\r\n\r\n'.encode())
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())

        elif request[0].upper() == "THEMELIST":
            if len(request) == 1:
                themelist_command(THEME, client_f)
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())

        elif request[0].upper() == "THEME":
            theme_command(THEME, ERRORS, client_f, request)

        # QUIT command
        elif request[0].upper() == "QUIT":
            if len(request) == 1:
                client_f.sendall(f'{THEME.response}Goodbye\r\n\r\n{THEME.end}'.encode())
                client_f.close()
                break
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}\r\n\r\n'.encode())

        # Check if other commands have been used
        elif request[0].upper() in ["LIST", "JOIN", "GET", "CREATE", "MESS", "LEAVE"]:
            client_f.sendall(f'{ERRORS.er_msg("2")}\r\n\r\n'.encode())

        else:
            client_f.sendall(f'{ERRORS.er_msg("0")}\r\n\r\n'.encode())

    client_f.close()


# Creating defoult channels
Channels("General", None, 50).create()
Channels("Programming", None, 50).create()
Channels("Music", None, 50).create()

# Starting server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(connection)
    s.listen(5)
    print(f'Server {connection[0]} started on port: {connection[1]}')
    while True:
        client, addr = s.accept()
        thread = threading.Thread(target=user_connect, args=(client, addr,))
        thread.start()
