from channels.generic.websocket import AsyncWebsocketConsumer
from .services import DeviceService
from .repositories import DeviceRepository
from asgiref.sync import sync_to_async
from .tasks import get_metrics_task
from celery.result import AsyncResult
import json
import asyncio
import logging

logger = logging.getLogger("system_monitor")

class DashboardConsumer(AsyncWebsocketConsumer):
    
    subscriptions = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.subscriptions is None:
            self.subscriptions = {}

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
        logger.debug(f"USER: '{self.user}', USER_ID: {self.user_id}, GROUP_NAME: {self.group_name}")

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
        logger.debug("Message received.")
        text_data_json = json.loads(text_data)
        logger.debug(f"Message: {text_data_json}")

        if text_data_json["type"] == "subscribe":
            try:
                device_name = text_data_json["data"]["device"]
                
                if device_name in self.subscriptions:
                    logger.debug(f"User '{self.user}' attempted to subscribe to device '{device_name}'. Subscription already exists.")

                    message = f"Already subscribed to device '{device_name}"
                    await self.send(text_data=json.dumps({
                        "type": "error",
                        "message": message
                    }))
                else:
                    logger.debug(f"User '{self.user}' subscribed to device '{device_name}'.")

                    result = get_metrics_task.delay(self.user_id, device_name)
                    task_id = result.id
                    self.subscriptions[device_name] = task_id

                    message = f"Successfully subscribed to device '{device_name}"
                    await self.send(text_data=json.dumps({
                        "type": "success",
                        "message": message
                    }))
            except Exception as e:
                logger.error(f"Error while subscribing to device '{device_name}' for user '{self.user}': {e}")

        if text_data_json["type"] == "unsubscribe":
            try:
                device_name = text_data_json["data"]["device"]

                if device_name not in self.subscriptions:
                    logger.debug(f"User '{self.user}' attempted to unsubscribe to device '{device_name}'. Subscription does not exists.")

                    message = f"Not subscribed to device '{device_name}"
                    await self.send(text_data=json.dumps({
                        "type": "error",
                        "message": message
                    }))
                else:
                    logger.debug(f"User '{self.user}' unsubscribed to device '{device_name}'.")

                    task_id = self.subscriptions[device_name]
                    AsyncResult(task_id).revoke(terminate=True)

                    message = f"Successfully unsubscribed to device '{device_name}'."
                    await self.send(text_data=json.dumps({
                        "type": "success",
                        "message": message
                    }))
            except Exception as e:
                logger.error(f"Error while unsubscribing to device '{device_name}' for user '{self.user}': {e}")
    
    async def get_metrics(self, device_name):
        try:
            logger.debug(f"get_metrics task created for user '{self.user}' and device '{device_name}'")

            device_repo_in = DeviceRepository()
            device_service = DeviceService(device_repo_in)
            
            while True:
                message = await sync_to_async(device_service.get_metrics)(self.user, device_name)

                if not message:
                    logger.debug("get_metrics task failed. No metrics data retrieved.")
                else:
                    logger.debug(f"get_metrics task completed. Metrics data retrieved.")

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
        
        logger.debug(f"Message sent.")