from src.config import generate_id



class User:
    def __init__(self, idCounter: int, name: str = "Guest"):
        self.id = generate_id(idCounter)
        self.name = f'{name}#{self.id}'

    def __str__(self) -> str:
        return self.name


class Users:
    def __init__(self) -> None:
        self.users = {}

    def create_user(self, name: str) -> None:
        """
        Add new user to users dictionary
        """
        if name not in self.users:
            user = User(len(self.users), name)
            self.users[user.id] = user
        else:
            # TODO: Add error handling
            return 
