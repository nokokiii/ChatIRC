ip = 'localhost'
port = 56990
connection = (ip, port)


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


def generate_id(counter):
    generated_id = hex(counter)[2:].zfill(2)
    counter += 1
    return generated_id


class Errors:
    bold = "\u001b[1m"
    red = "\u001b[0;31m"
    end = "\u001b[0m"

    messages = {
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

    def er_msg(self, error):
        return f"{self.bold}{self.red}{self.messages[error]}{self.end}"


class Themes:
    def __init__(self):
        self.theme = 'default'
        self.input = '\u001b[37m'
        self.bold = '\u001b[1m'
        self.response = '\u001b[37;1m'
        self.end = '\u001b[0m'
        self.error = '\u001b[31m'
        self.underline = '\u001b[4m'

    def change_theme(self, t):
        if t == 'pink':
            self.pink_theme()
        elif t == 'blue':
            self.blue_theme()
        elif t == 'green':
            self.green_theme()
        elif t == 'default':
            self.default_theme()

    def themes(self):
        return ['default', 'pink', 'blue', 'green'], self.theme

    def pink_theme(self):
        self.theme = 'pink'
        self.input = '\u001b[35m'
        self.response = '\u001b[35;1m'

    def blue_theme(self):
        self.theme = 'blue'
        self.input = '\u001b[34m'
        self.response = '\u001b[34;1m'

    def green_theme(self):
        self.theme = 'green'
        self.input = '\u001b[32m'
        self.response = '\u001b[32;1m'

    def default_theme(self):
        self.theme = 'default'
        self.input = '\u001b[37m'
        self.response = '\u001b[37;1m'


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
               "MESS - writes a message"

