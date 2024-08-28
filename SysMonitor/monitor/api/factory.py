from ninja import NinjaAPI
from clients import InputActivityAPIClient, APIClient

# Factory to produce APIClient instances
class APIClientFactory:
    @staticmethod
    def create_input_activity_client(api: NinjaAPI) -> APIClient:
        return InputActivityAPIClient(api)