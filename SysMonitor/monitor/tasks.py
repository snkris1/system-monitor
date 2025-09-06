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
    """
    A long-running Celery task to periodically fetch system metrics for a device
    and send them to the client via WebSockets.
    """
    logger.info(f"Starting metrics task for user_id '{user_id}' and device '{device_name}'")
    channel_layer = get_channel_layer()
    # Group name is used by Django Channels to broadcast messages to all consumers
    # that have subscribed to this group.
    group_name = f"device_{device_name.replace(' ', '_')}"

    try:
        device_repo_in = DeviceRepository()
        device_service = DeviceService(device_repo_in)
        user = get_user_by_id(user_id)

        if not user:
            logger.error(f"No user found with id {user_id}. Aborting task.")
            return

        while not self.is_aborted():
            try:
                message = device_service.get_metrics(user, device_name)

                if not message:
                    logger.warning(f"No metrics data retrieved for device '{device_name}'.")
                else:
                    logger.debug(f"Metrics retrieved for device '{device_name}'. Sending to group '{group_name}'.")
                    async_to_sync(channel_layer.group_send)(
                        group_name, {
                            "type": "send.metrics",
                            "message": message
                        }
                    )
                
                time.sleep(5)

            except Exception as e:
                # Log errors inside the loop to ensure the task continues running
                logger.error(f"Error in get_metrics loop for device '{device_name}': {e}", exc_info=True)
                # Wait before retrying to avoid spamming logs in case of a persistent error
                time.sleep(10)

        logger.info(f"Metrics task for device '{device_name}' was aborted.")

    except Exception as e:
        # Log any setup errors that occur before the loop starts
        logger.critical(f"Fatal error in get_metrics_task setup for device '{device_name}': {e}", exc_info=True)