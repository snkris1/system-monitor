from celery import shared_task
from celery.contrib.abortable import AbortableTask
from monitor.repositories import DeviceRepository
from monitor.services import DeviceService
from users.services import get_user_by_id
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
import time

logger = logging.getLogger("system_monitor")

@shared_task(bind=True, base=AbortableTask)
def get_metrics_task(self, user_id, device_name):
    try:
        logger.debug(f"get_metrics task created for user '{user}' and device '{device_name}'")

        self.channel_layer = get_channel_layer()

        device_repo_in = DeviceRepository()
        device_service = DeviceService(device_repo_in)
        user = get_user_by_id(user_id)
        
        while True:
            try:
                if self.is_aborted():
                    logger.warning(f"get_metrics task aborted for user '{user}' and device '{device_name}'")
                    return
                
                message = device_service.get_metrics(self.user, device_name)

                if not message:
                    logger.debug("get_metrics task failed. No metrics data retrieved.")
                else:
                    logger.debug(f"get_metrics task completed. Metrics data retrieved.")

                async_to_sync(self.channel_layer.group_send)(
                    self.group_name, {
                        "type": "send.metrics",
                        "message": message
                    }
                )
                
                time.sleep(5)
            except:
                pass
    except Exception as e:
        print(f"An error occurred during get_metrics task: {e}")
        # Revoke task