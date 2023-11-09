import __init__

from abc import *


class IMigrations(metaclass=ABCMeta):
    @abstractmethod
    def create_user(self):
        ...

    @abstractmethod
    def init_user(self):
        ...

    @abstractmethod
    def create_post(self):
        ...

    @abstractmethod
    def init_post(self):
        ...
