from typing import TYPE_CHECKING, List

import datetime
from socket import socket

from config import commands_help, protocol, read_data
from server.utils.themes import Themes

if TYPE_CHECKING:
    from server.utils.server import Server

class UserHandling:
    def __init__(self, client: socket, server: Server) -> None:
        self.client = client
        self.server = server
        self.theme = Themes()
        self.current_channel = None
        self.user = None

    # TODO: Implement one general method for sending messages to client based on style

    def help_cmd(self, scopre: str) -> None:
        """
        Logic for HELP command
        """
        # TODO: Implement patter mathcing to send help message based on scope (before hello, after hello, chat)

        # TODO: After implement method for sending messages refactor it to use it
        self.client.sendall(f"{self.THEME.response}{commands_help}{self.THEME.end}{protocol}".encode())

    def themelist_cmd(self) -> None:
        """
        Provide list of available themes
        """
        # TODO: After implement method for sending messages refactor it to use it
        print(self.theme.available_themes())

    def quit_cmd(self) -> None:
        """
        Logic for QUIT command
        """
        # TODO: Implement better way to quiting (close client, rmeove user from server, remove self [UserHandling])
        # self.client.sendall(f"{self.server.THEME.response}Goodbye{protocol}{self.server.THEME.end}".encode())
        # self.client.close()

        return

    def theme_cmd(self, request: list) -> None:
        if len(request) != 2:
            # TODO: Send error message
            return
        print(self.theme.change_theme(request[1].lower())) # TODO: Change this to send message to client

    def channel_list_cmd(self) -> None:
        """
        Provide channel list for user
        """
        # TODO: After implement method for sending messages refactor it to use it
        response = "The list of channels: \n".join(f"{channel} [{len(self.server.channels[channel].users)}/{self.server.channels[channel].max_users}] {'Private' if self.server.channels[channel].isLocked else ''} \n" for channel in self.server.channels)
        self.client.sendall(f"{response}{protocol}".encode())
    
    def channel_create_cmd(self, request: list) -> None:
        """
        CREATE command logic
        """
        def create_validation(request: list) -> bool:
            request_len = len(request)

            return (
                request_len == 1 or
                request_len > 4 or
                (request_len == 4 and not request[3].isdigit()) or
                (request_len == 4 and request[3].isdigit()) or
                (request_len == 3 and (request[2] == "" or request[2] != 0)) or
                (request_len == 3 and request[2] == "")
            )

        if create_validation(request):
            # TODO: Send error message
            return
        
        channel = request[1]
        max_users = int(request[3]) if len(request) == 4 else 10
        password = request[2]

        self.channels.create_channel(channel, password, max_users)
        response = f"{self.THEME.response}Channel {channel} created{self.THEME.end}{protocol}"
        self.client.sendall(response.encode())
        
    def mess_cmd(self, request):
        """
        MESS command logic
        """
        def mess_validation(request: list) -> bool:
            return len(request) > 2 or request[1] == ""
        
        def get_now() -> str:
            now = datetime.now().strftime("%B")
            now = datetime.strftime(f"%d {now[:3]} %H:%M:%S")

        if not mess_validation(request):
            # TODO: Send error
            return
        
        now = get_now()

        # Adding message to chat
        self.channel.add_message(f"[{now}] {self.user.name}: {request[1]}")

        # TODO: Send to client that message was sent

    def get_cmd(self, request: list) -> None:
        """
        GET command logic
        """
        # ! GET command logic [ 1 or 2 argument ]
        # Getting amount of messages to send
        # mess_amount = 10 if len(channels[channel].chat) > 10 else len(channels[channel].chat)

        # client.sendall((f'{channel} chat (last {mess_amount} messages)\r\n' + ''.join(
        #     f'{channels[channel].chat[(len(channels[channel].chat) - mess_amount) + i]}\r\n' for i in
        #     range(mess_amount)) + '\r\n').encode())
        
        pass

    def leave_cmd(self, request: list) -> None:
        """
        LEAVE command logic
        """
        # ! Leave command logiv [ 1 argument ]
        # # Removing user from channel
        # # TODO: Move this logic to server object
        # channels[channel].users.remove(user)

        # # Sending response to user
        # response = f'{Thm.response}Succesfully disconnected from {channel}{Thm.end}\r\n\r\n'
        # client.sendall(response.encode())
        # return
        pass

    def chat(self):
        """
        Main function for chat
        """
        while True:
            data = read_data(self.client).decode().strip(protocol)
            request = data.split('|')

            # TODO: Change this to pattern matching
            command = request[0].upper()

            # Matching cmds with more arguments and some invalid cmds
            match command:
                case None: return # TODO: return ERROR
                case "THEME": self.theme_cmd(request)
                case "MESS": self.mess_cmd(request)
                case "GET": self.get_cmd(request)
                case "HELP": self.help_cmd(scope="chat")
                case ["HELLO", "JOIN", "LIST", "CREATE"]: return # self.client.sendall(f"{self.ERRORS.er_msg("1")}{protocol}".encode()) # TODO: return ERROR
                # TODO: Add case with cmds you can't use in chat

            if len(request) != 1:
                # self.client.sendall(f"{self.ERRORS.er_msg("1")}{protocol}".encode())
                return

            # Matching cmds with 1 argument
            match command:
                case "THEMELIST": self.themelist_cmd()
                case "LEAVE": self.leave_cmd()
                case "QUIT": self.quit_cmd()
                case _: return                
            # MESS command {MESS|<message>}

# def join_command(client, request, user, channels, ER, Thm, datetime):
    def join_cmd(self, request: List):
        if len(request) == 1 or len(request) > 2:
            # self.client.sendall(f'{ER.er_msg("1")}\r\n\r\n'.encode())
            return
        
        channel_name = request[1]
        password = request[2] if len(request) == 3 else None

        # TODO: change error msg to error code so it can use method for error messages
        is_okay, error_code, self.channel = self.server.join_validation(channel_name, password)

        if not is_okay:
            # TODO: Print error based on error code
            return
        
        # Adding user to channel
        self.channel.add_user(self.user)

        # Sending response to user
        # TODO: Send response that user joined the channel
        # response = f'{Thm.response}Succesfully connected to {channel}{Thm.end}\r\n\r\n'
        # client.sendall(response.encode())

        # Chat Loop
        self.chat()
        

    def hello_cmd_match(self):
        data = read_data(self.client).decode().strip(f"{protocol}")
        request = data.split("|")
        command = request[0].upper()

        # TODO: First check commands that require some argument and then 1 len arguments so there is no need to reqpeat if
        # Matching cmds with more arguments and some invalid cmds
        match command:
            case None: return # TODO: return ERROR 
            # THEME command {THEME|<theme>}
            case "THEME": self.theme_cmd(request)
            # CREATE command {CREATE|<channel_name>|<password>|<max_users>}
            case "CREATE": self.channel_create_cmd(request)
            # JOIN command {JOIN|<channel>|<password>}
            case "JOIN": self.join_cmd(request)
            # join_command(self.client, request, self.user, self.channels, self.ERRORS, self.THEME, datetime)
            case ["GET", "MESS", "LEAVE"]: return # # self.client.sendall(f"{self.ERRORS.er_msg("4")}{protocol}".encode()) # TODO: return ERROR

        if len(request) != 1:
            # self.client.sendall(f"{self.ERRORS.er_msg("1")}{protocol}".encode())
            return
        
        match command:
            # HELP command {HELP}
            case "HELP": self.help_cmd()
            # THEMELIST command {THEMELIST}
            case "THEMELIST": self.themelist_cmd()
            # QUIT command {QUIT}
            case "QUIT": self.quit_cmd()
            # LIST command {LIST}
            case "LIST": self.channel_list_cmd()
            # Invalid command
            case _: pass # self.client.sendall(f"{self.ERRORS.er_msg("0")}{protocol}".encode())

    def hello_command(self, request: list) -> None:
        if len(request) == 2:
            # self.client.sendall(f"{self.ERRORS.er_msg("1")}{protocol}".encode())
            return
        
        # Sending error if user doesn"t provide username
        user = self.server.users.create_user(request[1])
        response = f"{self.THEME.style(f'HELLO {user.name}', 'response')}{protocol}"
        self.client.sendall(response.encode())

        while True:
            self.hello_cmd_match(self.client, user)

    def command_match_1(self, command: str, request: list) -> bool:
        match command.upper():
            case "HELLO":
                self.hello_command(self.client, request)
            case "HELP":
                self.help_cmd(command, self.client)
            case "THEMELIST":
                self.themelist_cmd(self.client, command)
            case "THEME":
                self.theme_command(self.THEME, self.ERRORS, self.client, command)
            case "QUIT":
                self.quit_cmd(self.client, command)
                return False
            case ("LIST", "JOIN", "GET", "CREATE", "MESS", "LEAVE"):
                pass
                # self.client.sendall(f"{self.ERRORS.er_msg("2")}{protocol}".encode())
            case _:
                pass
                # self.client.sendall(f"{self.ERRORS.er_msg("0")}{protocol}".encode())

        return True

    def handle(self):
        """
        Handle user connection
        """
        run = True
        while run:
            data = read_data(self.client).decode().strip("{protocol}")
            request = data.split("|")

            if not self.command_match_1(request[0], self.client):
                break