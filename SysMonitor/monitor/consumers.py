from channels.generic.websocket import AsyncWebsocketConsumer
from .services import DeviceService
from .repositories import DeviceRepository
import json
import asyncio
import logging

logger = logging.getLogger("system_monitor")

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self): 
        # TODO: ENSURE USER IS AUTH AND USER EXISTS
        self.user = self.scope['user']
        self.user_id = self.scope['user'].id
        self.group_name = f"user-{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

        logger.info("Dashboard websocket connection established.")

    async def disconnect(self, close_code):
        self.send_task.cancel() # TODO: LEARN WHEN TO PROPERLY USE AWAIT AND ASYNC
        try: 
            await self.send_task
        except asyncio.CancelledError:
            logger.debug("Send metrics task cancelled.")

        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

        logger.info("Dashboard websocket disconnected.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json["type"] == "subscribe":
            try:
                self.send_task = asyncio.create_task(self.get_metrics(text_data_json["data"]["device"])) # TODO: LOOK INTO CELERY
            except Exception as e:
                await self.send_task.cancel()

        if text_data_json["type"] == "unsubscribe":
            self.send_task.cancel()
            try:
                await self.send_task
            except asyncio.CancelledError:
                logger.debug("Send metrics task cancelled.")
            except Exception as e:
                logger.error(f"Error while awaiting send_task: {e}")
    
    async def get_metrics(self, device_name):
        try:
            device_repo_in = DeviceRepository()
            device_service = DeviceService(device_repo_in)
            
            while True:
                message = await device_service.get_metrics(self.user, device_name) # data should be in deserialized form... maybe

                await self.channel_layer.group_send(
                    self.group_name, {
                        "type": "send.metrics",
                        "message": message
                    }
                )
                
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            logger.debug("get_metrics task cancelled during disconnection.")
            # TODO: WOULD THIS BE A ERROR?

    async def send_metrics(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "type": "metrics",
            "message": message
            }))