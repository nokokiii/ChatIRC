import socket
import threading
from datetime import datetime

from config import connection, read_data, \
    Errors, commands_help, theme_command, themelist_command, join_command, protocol
from src.server.utils.themes import Themes
from src.server.utils.users import User, Users
from src.server.utils.channels import Channel, Channels

ERRORS = Errors()
THEME = Themes()

users = Users()
channels = Channels()

def hello_command(client_f):
    if len(request) == 2:
        client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())
        return
    
    # Sending error if user doesn't provide username
    user = Users(request[1]) if request[1] else Users()
    users[user.id] = user
    response = f'{THEME.style(f"HELLO {user.name}", "response")}{protocol}'
    client_f.sendall(response.encode())

    while True:
        data = read_data(client_f).decode().strip(f'{protocol}')
        request = data.split('|')

        # HELLO command {HELLO|<name>}
        if request[0].upper() == "HELLO":
            client_f.sendall(f'{ERRORS.er_msg("3")}{protocol}'.encode())

        elif request[0].upper() == "THEME":
            theme_command(THEME, ERRORS, client_f, request)

        elif request[0].upper() == "THEMELIST":
            if len(request) == 1:
                themelist_command(THEME, client_f)
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())

        elif request[0].upper() == "HELP":
            if len(request) == 1:
                client_f.sendall(f'{THEME.response}{commands_help}{THEME.end}{protocol}'.encode())
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())

        # LIST command {LIST}
        elif request[0].upper() == "LIST":
            if len(request) == 1:
                response = 'The list of channels\r\n'
                for channel in channels:
                    privacy = 'Private' if channels[channel].isLocked else 'Public'
                    response += f'{channel} [{len(channels[channel].users)}/{channels[channel].max_users}] {privacy}\r\n'
                response += f'{THEME.end}{protocol}'
                client_f.sendall(response.encode())
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())

        # CREATE command {CREATE|<channel_name>|<password>|<max_users>}
        elif request[0].upper() == "CREATE":
            if len(request) == 1 or len(request) > 4 or request[1] == "" or len(request) == 4 and not request[3].isdigit() or len(request) == 3 and request[2] == "" or len(request) == 4 and request[3].isdigit() or len(request) == 3 and request[2] != 0:
                client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())
            else:
                channel = str(request[1]).replace(" ", "")
                password = str(request[2]) if len(request) >= 3 else None
                max_users = int(request[3]) if len(request) == 4 else 10
                # Checking if channel already exists
                if f'#{channel}' in channels:
                    response = f'{ERRORS.er_msg("9")}{protocol}'
                else:
                    # Creating new channel
                    new_channel = Channels(channel, password, max_users)
                    new_channel.create()
                    response = f'{THEME.response}Channel {channel} created{THEME.end}{protocol}'

                client_f.sendall(response.encode())

        # JOIN command {JOIN|<channel>|<password>}
        elif request[0].upper() == "JOIN":
            join_command(client_f, request, user, channels, ERRORS, THEME, datetime)

        # Sending error if user try to use GET or MESS command while not being connected to channel
        elif request[0].upper() in ["GET", "MESS", "LEAVE"]:
            client_f.sendall(f'{ERRORS.er_msg("4")}{protocol}'.encode())

        # Invalid command
        else:
            client_f.sendall(f'{ERRORS.er_msg("0")}{protocol}'.encode())

def user_connect(client_f, addr_f):
    print(f'Connected with {addr_f[0]}')

    while True:
        data = read_data(client_f).decode().strip('{protocol}')
        request = data.split('|')

        # HELLO command {HELLO|<name>}
        if request[0].upper() == "HELLO":
            hello_command(client_f)           

        # HELP command
        elif request[0].upper() == "HELP":
            if len(request) == 1:
                client_f.sendall(f'{THEME.response}{commands_help}{THEME.end}{protocol}'.encode())
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())

        elif request[0].upper() == "THEMELIST":
            if len(request) == 1:
                themelist_command(THEME, client_f)
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())

        elif request[0].upper() == "THEME":
            theme_command(THEME, ERRORS, client_f, request)

        # QUIT command
        elif request[0].upper() == "QUIT":
            if len(request) == 1:
                client_f.sendall(f'{THEME.response}Goodbye{protocol}{THEME.end}'.encode())
                client_f.close()
                break
            else:
                client_f.sendall(f'{ERRORS.er_msg("1")}{protocol}'.encode())

        # Check if other commands have been used
        elif request[0].upper() in ["LIST", "JOIN", "GET", "CREATE", "MESS", "LEAVE"]:
            client_f.sendall(f'{ERRORS.er_msg("2")}{protocol}'.encode())

        else:
            client_f.sendall(f'{ERRORS.er_msg("0")}{protocol}'.encode())

    client_f.close()


def create_default_channels() -> None:
    """
    Create default channels    
    """
    Channels("General", None, 50).create()
    Channels("Programming", None, 50).create()
    Channels("Music", None, 50).create()


def run_server() -> None:
    """
    Main function for running whole server
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(connection)
        s.listen(5)
        print(f'Server {connection[0]} started on port: {connection[1]}')

        while True:
            client, addr = s.accept()
            thread = threading.Thread(target=user_connect, args=(client, addr,))
            thread.start()


if __name__ == '__main__':
    create_default_channels()
    run_server()
