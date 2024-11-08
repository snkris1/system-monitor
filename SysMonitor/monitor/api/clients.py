from typing import Protocol
from ninja import NinjaAPI
from .schemas import InputActivitySchema, InputActivityCreateSchema

# Interface (Protocol) for API Clients
class APIClient(Protocol):
    def fetch_all_activities(self) -> list[InputActivitySchema]:
        ...

    def fetch_activity_by_timestamp(self, timestamp: str) -> InputActivitySchema:
        ...

    def create_activity(self, input_activity: InputActivityCreateSchema) -> InputActivitySchema:
        ...

# Concrete implementation of the APIClient
class InputActivityAPIClient:
    def __init__(self, api: NinjaAPI):
        self.api = api

    def fetch_all_activities(self) -> list[InputActivitySchema]:
        return self.api.get("/input_activity").json()

    def fetch_activity_by_timestamp(self, timestamp: str) -> InputActivitySchema:
        return self.api.get(f"/input_activity/{timestamp}").json()

    def create_activity(self, input_activity: InputActivityCreateSchema) -> InputActivitySchema:
        return self.api.post("/input_activity", json=input_activity.dict()).json()
