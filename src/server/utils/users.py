from src.config import generate_id


class Users:
    def __init__(self) -> None:
        self.users = {}

    def add_new_user(self, name: str) -> None:
        """
        Add new user to users dictionary
        """
        if name not in self.users:
            self.users[name] = User(len(self.users), name)
        else:
            # TODO: Add error handling
            return 


class User:
    def __init__(self, idCounter: int, name: str = "Guest"):
        self.id = generate_id(idCounter)
        self.name = f'{name}#{self.id}'
        