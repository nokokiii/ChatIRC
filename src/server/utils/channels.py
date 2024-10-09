from typing import Optional

class Channel:
    def __init__(self, name: str, max_users: int, password: Optional[str] = None) -> None:
        self.name = name
        self.password = password
        self.max_users = max_users if max_users and max_users > 0 else 10
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
    
    def format_password(self, password: str) -> Optional[str]:
        """
        Check if password format is correct
        """
        return None if len(password) < 4 else password

    def create_channel(self, name: str, password: Optional[str], max_users: int) -> None:
        """
        Create new channel
        """
        name = self.format_name(name)
        password = self.format_password(name, password)

        if name not in self.channels:
            self.channels[name] = Channel(name, max_users, password)
        else:
            # Write Error [9]
            return

    def get_channel(self, name: str) -> Channel:
        """
        Get channel by name
        """
        return self.channels[name]
