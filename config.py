IP = 'localhost'
PORT = 53496

connection = (IP, PORT)
protocol = '\r\n\r\n'

# TODO: Split this file to server and client. Add some congig file (not python) for protocol and connection

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

