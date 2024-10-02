IP = 'localhost'
PORT = 53496

connection = (IP, PORT)
protocol = '\r\n\r\n'

# Server commands functions
def theme_command(Thm, ER, client_f, request):
    if len(request) == 2:
        if request[1].lower() in Thm.themes()[0]:
            Thm.change_theme(request[1].lower())
            client_f.sendall(f'{Thm.response}Theme changed to {Thm.theme}{Thm.end}\r\n\r\n'.encode())
        else:
            client_f.sendall(f'{ER.er_msg("12")}\r\n\r\n'.encode())
    else:
        client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())


def themelist_command(Thm, client_f):
    themes, current_theme = Thm.themes()
    resposne = f'{Thm.response} List of themes: \r\n'
    for i in themes:
        if i == current_theme:
            resposne += f'>{Thm.bold} {i}\r\n'
        else:
            resposne += f'{i}\r\n'
    resposne += f'{Thm.end}\r\n\r\n'
    client_f.sendall(resposne.encode())


def read_data(socket):
    data = b''
    while b'\r\n\r\n' not in data:
        data += socket.recv(1)

    return data


def generate_id(counter: int) -> str:
    """
    Generate hex id for user
    """
    generated_id = hex(counter)[2:].zfill(2)
    counter += 1
    return generated_id


def join_command(client_f, request, user, channels, ER, Thm, datetime):
    if len(request) == 1 or len(request) > 2:
        client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())
        return
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
                        if len(request) == 1 or len(request) > 2:
                            client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())
                        elif len(request) == 2:
                            theme_command(Thm, ER, client_f, request)

                    # THEMELIST command {THEMELIST}
                    elif request[0].upper() == "THEMELIST":
                        if len(request) == 1:
                            themelist_command(Thm, client_f)
                        else:
                            client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())

                    elif request[0].upper() == "LEAVE":
                        if len(request) == 1:
                            # Removing user from channel
                            channels[channel].users.remove(user)

                            # Sending response to user
                            response = f'{Thm.response}Succesfully disconnected from {channel}{Thm.end}\r\n\r\n'
                            client_f.sendall(response.encode())
                            return
                        else:
                            client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())

                    # Sending error if user try to use LIST, JOIN or CREATE command
                    elif request[0].upper() == "LIST" or request[0].upper() == "JOIN" or request[0].upper() == "CREATE":
                        client_f.sendall(f'{ER.er_msg("11")}\r\n\r\n'.encode())

                    # MESS command {MESS|<message>}
                    elif request[0].upper() == "MESS":
                        if len(request) == 1 or request[1] == "" or len(request) > 2:
                            client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())
                        else:
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
                        if len(request) == 1:
                            # Getting amount of messages to send
                            mess_amount = 10 if len(channels[channel].chat) > 10 else len(channels[channel].chat)

                            # Creating response <3 <3 lovki for this line <3 <3
                            client_f.sendall((f'{channel} chat (last {mess_amount} messages)\r\n' + ''.join(
                                f'{channels[channel].chat[(len(channels[channel].chat) - mess_amount) + i]}\r\n' for i in
                                range(mess_amount)) + '\r\n').encode())
                        else:
                            client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())

                    # HELP command {HELP}
                    elif request[0].upper() == "HELP":
                        if len(request) == 1:
                            client_f.sendall(f'{Thm.response}{commands_help}{Thm.end}\r\n\r\n'.encode())
                        else:
                            client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())

                    # QUIT command {QUIT}
                    elif request[0].upper() == "QUIT":
                        if len(request) == 1:
                            client_f.sendall(f'{Thm.response}Goodbye!!{Thm.end}\r\n\r\n'.encode())
                            client_f.close()
                            break
                        else:
                            client_f.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())

                    # Invalid command
                    else:
                        client_f.sendall(f'{ER.er_msg("0")}\r\n\r\n'.encode())
            else:
                # Sending response to user if password is incorrect
                client_f.sendall(f'{ER.er_msg("7")}\r\n\r\n'.encode())
    else:
        # Sending response to user if channel doesn't exist
        client_f.sendall(f'{ER.er_msg("6")}\r\n\r\n'.encode())


class Errors:

    def er_msg(self, error):
        return f"{self.bold}{self.red}{self.messages[error]}{self.end}"

ERRORS = {
    '0': 'Error 0: Invalid command',
    '1': 'Error 1: Invalid arguments',
    '2': 'Error 2: You have to be logged to use this command',
    '3': 'Error 3: You are already logged in',
    '4': 'Error 4: You have to be in chat to use this command',
    '5': 'Error 5: You are already in chat',
    '6': 'Error 6: No such chat',
    '7': 'Error 7: Password is incorrect',
    '8': 'Error 8: The channel name is invalid',
    '9': 'Error 9: The channel already exists',
    '10': 'Error 10: The channel is full',
    '11': 'Error 11: You can not use this command while being connected to channel',
    '12': 'Error 12: There is no such a theme'
}

commands_help = "List of commands: \r\n" \
               "HELLO - to connect to the server\r\n" \
               "HELP - Shows the list of commands\r\n" \
               "THEME - to change theme\r\n" \
               "THEMELIST - to get list of themes\r\n" \
               "LIST - to get list of channels\r\n" \
               "CREATE - to create new channel\r\n" \
               "JOIN - to join channel\r\n" \
               "QUIT - to disconnect from the server\r\n" \
               "GET - prints out the last 10 messeges\r\n" \
               "MESS - writes a message\r\n" \
               "LEAVE - to leave channel"

