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

    def create_channel(self, name, password, max_users):
        if name not in self.channels:
            self.channels[name] = Channel(name, password, max_users)
        else:
            return

    def get_channel(self, name):
        return self.channels[name]
