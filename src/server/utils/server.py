from typing import Tuple

from socket import socket

from src.server.utils.channels import Channels
from src.server.utils.users import Users
from src.server.utils.user_handler import UserHandling



class Server:
    def __init__(self, connection: Tuple[str, int]) -> None:
        self.connection = connection
        self.users = Users()
        self.channels = Channels()
        # TODO : Fix errors
        # self.ERRORS = Errors()

    def handle_new_user(self, client: socket, addr) -> None:
        print(f'Connected with {addr[0]}')

        user_handler = UserHandling(client, self)
        user_handler.handle()
        
        client.close()


    def create_default_channels(self) -> None:
        """
        Create default channels    
        """
        self.channels.create_channel("General", None, 50)
        self.channels.create_channel("General 2nd", None, 50)
        self.channels.create_channel("General 3rd", None, 50)
