from abc import ABC, abstractmethod


class CommonProtocol(ABC):
    @abstractmethod
    def create_new_admin_user_session(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_resources(self, *args, **kwargs):
        pass

    @abstractmethod
    def reserve_resource(self, resource_id, *args, **kwargs):
        pass

    @abstractmethod
    def release_resource(self, resource_id, *args, **kwargs):
        pass

    @abstractmethod
    def create_new_admin_user_session(self, *args, **kwargs):
        pass
