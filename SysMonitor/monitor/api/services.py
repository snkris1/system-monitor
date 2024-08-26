from .schemas import InputActivitySchema, InputActivityCreateSchema
from clients import APIClient

class InputActivityService:
    def __init__(self, client: APIClient):
        self.client = client

    def get_all_activities(self) -> list[InputActivitySchema]:
        return self.client.fetch_all_activities()

    def get_activity_by_timestamp(self, timestamp: str) -> InputActivitySchema:
        return self.client.fetch_activity_by_timestamp(timestamp)

    def add_new_activity(self, keyboard_activity: int, mouse_activity: int) -> InputActivitySchema:
        new_activity = InputActivityCreateSchema(
            keyboard_activity=keyboard_activity,
            mouse_activity=mouse_activity
        )
        return self.client.create_activity(new_activity)

    def plot_activities(self):
        activities = self.get_all_activities()
        if not activities:
            print("No activities to plot.")
            return

        timestamps = [activity.timestamp for activity in activities]
        keyboard_activities = [activity.keyboard_activity for activity in activities]
        mouse_activities = [activity.mouse_activity for activity in activities]

        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, keyboard_activities, label="Keyboard Activity")
        plt.plot(timestamps, mouse_activities, label="Mouse Activity")
        plt.xlabel("Timestamp")
        plt.ylabel("Activity Count")
        plt.title("User Input Activities Over Time")
        plt.legend()
        plt.show()
