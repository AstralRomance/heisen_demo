from abc import ABC, abstractmethod


class CommonProtocol(ABC):
    @abstractmethod
    def create_new_admin_user_session(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_resources(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def reserve_resource(self, resource_config, user_data, *args, **kwargs):
        pass

    @abstractmethod
    def wait_deploy(self, reservation_id, reserver_id):
        pass

    @abstractmethod
    def release_resource(self, reservation_id, *args, **kwargs):
        pass

    @abstractmethod
    def get_resource_status(self, resource_model, *args, **kwargs):
        pass

    @abstractmethod
    def get_active_user_reservations(self, user_id, *args, **kwargs):
        pass
