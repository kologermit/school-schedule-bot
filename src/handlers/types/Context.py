# Модуль контекста 

from models import User, Message

class Context:
    user: User
    message: Message
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
