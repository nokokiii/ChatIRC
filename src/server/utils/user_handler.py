from socket import socket

from src.config import commands_help, protocol, read_data
from src.server.utils.server import Server
from src.server.utils.themes import Themes


class UserHandling:
    def __init__(self, client: socket, server: Server) -> None:
        self.client = client
        self.server = server
        self.theme = Themes()
        self.user = None

    
    def create_validation(self, request: list) -> bool:
        """
        Check if CREATE command is valid
        """
        return len(request) == 1 or len(request) > 4 or request[1] == "" or len(request) == 4 and not request[3].isdigit() or len(request) == 3 and request[2] == "" or len(request) == 4 and request[3].isdigit() or len(request) == 3 and request[2] != 0


    def help_cmd(self) -> None:
        """
        Logic for HELP command
        """
        self.client.sendall(f'{self.THEME.response}{commands_help}{self.THEME.end}{protocol}'.encode())

    def themelist_cmd(self):
        print(self.theme.available_themes())

    def quit_cmd(self):
        self.client.sendall(f'{self.server.THEME.response}Goodbye{protocol}{self.server.THEME.end}'.encode())
        self.client.close()

    def theme_cmd(self, request):
        if len(request) == 2:
            print(self.theme.change_theme(request[1].lower()))
        else:
            # ERROR 1
            pass

    def channel_list_cmd():
        """
        Provide channel list for user
        """
        # if len(request) == 1:
        #         response = 'The list of channels\r\n'
        #         for channel in self.server.channels:
        #             privacy = 'Private' if self.server.channels[channel].isLocked else 'Public'
        #             response += f'{channel} [{len(self.server.channels[channel].users)}/{self.server.channels[channel].max_users}] {privacy}\r\n'
        #         response += f'{self.THEME.end}{protocol}'
        #         self.client.sendall(response.encode())
        #     else:
        #         self.client.sendall(f'{self.ERRORS.er_msg("1")}{protocol}'.encode())

        pass

    def channel_create_cmd(request):
        # if self.create_validation(request):
        #         self.client.sendall(f'{self.ERRORS.er_msg("1")}{protocol}'.encode())
        #         return
        # max_users = int(request[3]) if len(request) == 4 else 10
        # password = request[2]

        # self.channels.create_channel(channel, password, max_users)
        # response = f'{self.THEME.response}Channel {channel} created{self.THEME.end}{protocol}'
        # self.client.sendall(response.encode())
        pass
        
    def join_cmd(request):
        pass

    def hello_run(self):
        data = read_data(self.client).decode().strip(f'{protocol}')
        request = data.split('|')
        command = request[0].upper()

        # TODO: First check commands that require some argument and then 1 len arguments so there is no need to reqpeat if
        # Checking cmd with arguments
        match command:
            # THEME command {THEME|<theme>}
            case "THEME": self.theme_cmd(request)
            # CREATE command {CREATE|<channel_name>|<password>|<max_users>}
            case "CREATE": self.channel_create_cmd(request)
            # JOIN command {JOIN|<channel>|<password>}
            case "JOIN": self.join_cmd(request)
            # join_command(self.client, request, self.user, self.channels, self.ERRORS, self.THEME, datetime)

        if len(request) != 1:
            self.client.sendall(f'{self.ERRORS.er_msg("1")}{protocol}'.encode())
            return
        elif command in ["GET", "MESS", "LEAVE"]:
            self.client.sendall(f'{self.ERRORS.er_msg("4")}{protocol}'.encode())
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
            case _: self.client.sendall(f'{self.ERRORS.er_msg("0")}{protocol}'.encode())

    def hello_command(self, request: list) -> None:
        if len(request) == 2:
            self.client.sendall(f'{self.ERRORS.er_msg("1")}{protocol}'.encode())
            return
        
        # Sending error if user doesn't provide username
        user = self.server.users.create_user(request[1])
        response = f'{self.THEME.style(f"HELLO {user.name}", "response")}{protocol}'
        self.client.sendall(response.encode())

        while True:
            self.hello_run(self.client, user)

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
                self.client.sendall(f'{self.ERRORS.er_msg("2")}{protocol}'.encode())
            case _:
                self.client.sendall(f'{self.ERRORS.er_msg("0")}{protocol}'.encode())

        return True

    def handle(self):
        run = True
        while run:
            data = read_data(self.client).decode().strip('{protocol}')
            request = data.split('|')

            if not self.command_match_1(request[0], self.client):
                break