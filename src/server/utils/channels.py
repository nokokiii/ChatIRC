from typing import Optional

class Channel:
    def __init__(self, name, max_users, password = None):
        self.name = name
        self.password = password
        self.max_users = max_users
        self.isLocked = bool(password)
        self.users = []
        self.chat = []


class Channels:
    def __init__(self):
        self.channels = {}

    def format_name(self, name: str) -> str:
        """
        Format channel name
        """
        return name.replace(" ", "")
    
    def format_password(self, channel, password: str) -> Optional[str]:
        """
        Check if password format is correct
        """
        return None if len(password) < 4 else password

    def create_channel(self, name, password, max_users):
        """
        Create new channel
        """
        if name not in self.channels:
            self.channels[name] = Channel(name, password, max_users)
        else:
            # Write Error [9]
            return

    def get_channel(self, name):
        """
        Get channel by name
        """
        return self.channels[name]
