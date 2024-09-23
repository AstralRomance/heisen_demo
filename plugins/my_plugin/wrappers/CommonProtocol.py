from abc import ABC, abstractmethod


class CommonProtocol(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_record(self, data):
        pass
