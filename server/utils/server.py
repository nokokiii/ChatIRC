from typing import Tuple, List, Optional

from socket import socket

from server.utils.channels import Channels, Channel
from server.utils.users import Users
from server.utils.user_handler import UserHandling



class Server:
    def __init__(self, connection: Tuple[str, int]) -> None:
        self.connection = connection
        self.users = Users()
        self.channels = Channels()
        # TODO : Fix errors
        # self.ERRORS = Errors()

    def join_validation(self, channel_name: str, password: Optional[str]) -> Tuple[Tuple[bool, Optional[int]], Optional[Channel]]:
        """
        Validate if user can join the channel
        """
        # TODO: Implement returing correct error codes

        channel = self.channels.get_channel(channel_name)

        if channel is None:
            return (False, 0), None
        elif channel.is_max_users():
            return (False, 1), None

        if channel.is_locked and channel.password_validation(channel_name, password):
            return (False, 2), None
        
        return (True, None), channel

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
