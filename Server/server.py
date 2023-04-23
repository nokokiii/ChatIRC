import socket
import threading
from datetime import datetime
from config import connection, read_data, generate_id, \
    Errors, Themes, commands_help, theme_command, themelist_command

ER = Errors()
Thm = Themes()

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
                response = f'{Thm.response}HELLO {user.name}{Thm.end}\r\n\r\n'
                client_f.sendall(response.encode())

                while True:
                    data = read_data(client_f).decode().strip('\r\n\r\n')
                    request = data.split('|')

                    # HELLO command {HELLO|<name>}
                    if request[0].upper() == "HELLO":
                        client_f.sendall(f'{ER.er_msg("3")}\r\n\r\n'.encode())

                    elif request[0].upper() == "THEME":
                        theme_command(Thm, ER, client_f, request)

                    elif request[0].upper() == "THEMELIST":
                        themelist_command(Thm, client_f)

                    elif request[0].upper() == "HELP":
                        response = f'{Thm.response}{commands_help}{Thm.end}\r\n\r\n'
                        client_f.sendall(response.encode())

                    # LIST command {LIST}
                    elif request[0].upper() == "LIST":
                        # Sending list of channels
                        # response = 'THE LIST OF CHANNELS\r\n' + ''.join([f'{channel}\r\n' for channel in channels]) + '\r\n'
                        response = 'The list of channels\r\n'
                        for channel in channels:
                            privacy = 'Private' if channels[channel].isLocked else 'Public'
                            response += f'{channel} [{len(channels[channel].users)}/{channels[channel].max_users}] {privacy}\r\n'

                        response += f'{Thm.end}\r\n\r\n'
                        client_f.sendall(response.encode())

                    # CREATE command {CREATE|<channel_name>|<password>|<max_users>}
                    elif request[0].upper() == "CREATE":
                        if len(request) < 2:
                            client_f.sendall(f'{ER.er_msg("8")}\r\n\r\n'.encode())
                        else:
                            channel = request[1]
                            password = request[2] if len(request) >= 3 else None
                            max_users = int(request[3]) if len(request) == 4 else 10
                            # Checking if channel already exists
                            if f'#{channel}' in channels:
                                response = f'{ER.er_msg("9")}\r\n\r\n'
                            else:
                                # Creating new channel
                                new_channel = Channels(channel, password, max_users)
                                new_channel.create()
                                response = f'{Thm.response}Channel {channel} created{Thm.end}\r\n\r\n'

                            client_f.sendall(response.encode())

                    # JOIN command {JOIN|<channel>|<password>}
                    elif request[0].upper() == "JOIN":
                        channel = request[1]  # Getting channel name
                        password = request[2] if len(request) == 3 else None  # Getting password

                        if channel in channels:  # Checking if channel exists
                            if channels[channel].max_users <= len(channels[channel].users):  # Checking if channel is full
                                response = ER.er_msg('10')
                                client_f.sendall(f'{response}\r\n\r\n'.encode())
                            else:
                                if not channels[channel].isLocked or channels[channel].password == password:  # Checking if password is correct
                                    # Adding user to channel
                                    channels[channel].users.append(user)

                                    # Sending response to user
                                    response = f'{Thm.response}Succesfully connected to {channel}{Thm.end}\r\n\r\n'
                                    client_f.sendall(response.encode())

                                    while True:
                                        data = read_data(client_f).decode().strip('\r\n\r\n')
                                        request = data.split('|')

                                        # Sending error if user try to use HELLO command again
                                        if request[0].upper() == "HELLO":
                                            client_f.sendall(f'{ER.er_msg("3")}\r\n\r\n'.encode())

                                        # THEME command {THEME|<theme>}
                                        elif request[0].upper() == "THEME":
                                            theme_command(Thm, ER, client_f, request)

                                        # THEMELIST command {THEMELIST}
                                        elif request[0].upper() == "THEMELIST":
                                            themelist_command(Thm, client_f)

                                        # Sending error if user try to use LIST, JOIN or CREATE command
                                        elif request[0].upper() == "LIST" or request[0].upper() == "JOIN" or request[0].upper() == "CREATE":
                                            client_f.sendall(f'{ER.er_msg("11")}\r\n\r\n'.encode())

                                        # MESS command {MESS|<message>}
                                        elif request[0].upper() == "MESS":
                                            # Getting current date and time
                                            now = datetime.now()  # current date and time
                                            short_date = now.strftime("%B")
                                            dt_string = now.strftime(f"%d {short_date[:3]} %H:%M:%S")
                                            # Creating message text and adding it to the channel
                                            channels[channel].chat.append(f'[{dt_string}] {user.name}: {request[1]}')

                                            # Sending response to user that message was sent
                                            client_f.sendall(f'{Thm.response}Message sent{Thm.end}\r\n\r\n'.encode())

                                        # GET command {GET}
                                        elif request[0].upper() == "GET":
                                            # Getting amount of messages to send
                                            mess_amount = 10 if len(channels[channel].chat) > 10 else len(channels[channel].chat)

                                            # Creating response <3 <3 lovki for this line <3 <3
                                            client_f.sendall((f'{channel} chat (last {mess_amount} messages)\r\n' + ''.join(f'{channels[channel].chat[(len(channels[channel].chat) - mess_amount) + i]}\r\n' for i in range(mess_amount)) + '\r\n').encode())

                                        # HELP command {HELP}
                                        elif request[0].upper() == "HELP":
                                            client_f.sendall(f'{Thm.response}{commands_help}{Thm.end}\r\n\r\n'.encode())

                                        # QUIT command {QUIT}
                                        elif request[0].upper() == "QUIT":
                                            client_f.sendall(f'{Thm.response}Goodbye!!{Thm.end}\r\n\r\n'.encode())
                                            client_f.close()
                                            break

                                        # Invalid command
                                        else:
                                            client_f.sendall(f'{ER.er_msg("0")}\r\n\r\n'.encode())
                                else:
                                    # Sending response to user if password is incorrect
                                    client_f.sendall(f'{ER.er_msg("7")}\r\n\r\n'.encode())
                        else:
                            # Sending response to user if channel doesn't exist
                            client_f.sendall(f'{ER.er_msg("6")}\r\n\r\n'.encode())

                    # Sending error if user try to use GET or MESS command while not being connected to channel
                    elif request[0].upper() in ["GET", "MESS"]:
                        client_f.sendall(f'{ER.er_msg("4")}\r\n\r\n'.encode())

                    # Invalid command
                    else:
                        client_f.sendall(f'{ER.er_msg("0")}\r\n\r\n'.encode())
            else:
                # Sending error if user doesn't provide username
                client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())

        # HELP command
        elif request[0].upper() == "HELP":
            client_f.sendall(f'{Thm.response}{commands_help}{Thm.end}\r\n\r\n'.encode())
            
        elif request[0].upper() == "THEMELIST":
            themelist_command(Thm, client_f)

        elif request[0].upper() == "THEME":
            theme_command(Thm, ER, client_f, request)

        # QUIT command
        elif request[0].upper() == "QUIT":
            client_f.sendall(f'{Thm.response}Goodbye\r\n\r\n{Thm.end}'.encode())
            client_f.close()
            break

        # Check if other commands have been used
        elif request[0].upper() in ["LIST", "JOIN", "GET", "CREATE", "MESS"]:
            client_f.sendall(f'{ER.er_msg("2")}\r\n\r\n'.encode())

        else:
            client_f.sendall(f'{ER.er_msg("0")}\r\n\r\n'.encode())

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
