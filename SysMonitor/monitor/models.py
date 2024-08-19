from django.db import models
from django.utils import timezone

# Model to track system performance metrics
class SystemPerformance(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    cpu_usage = models.FloatField(help_text="CPU usage as a percentage")
    memory_usage = models.FloatField(help_text="Memory usage in MB")
    disk_activity = models.FloatField(help_text="Disk activity in MB/s")
    network_bandwidth = models.FloatField(help_text="Network bandwidth usage in Mbps")

    def __str__(self):
        return f"System Performance at {self.timestamp}"

    class Meta:
        verbose_name_plural = "System Performance"
        ordering = ['-timestamp']


# Model to track network activity
class NetworkActivity(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    connection_type = models.CharField(max_length=50, help_text="Type of connection, e.g., HTTP, FTP")
    inbound_traffic = models.FloatField(help_text="Inbound traffic in MB")
    outbound_traffic = models.FloatField(help_text="Outbound traffic in MB")
    data_transfer_rate = models.FloatField(help_text="Data transfer rate in MB/s")
    active_connections = models.IntegerField(help_text="Number of active connections")

    def __str__(self):
        return f"Network Activity at {self.timestamp}"

    class Meta:
        verbose_name_plural = "Network Activities"
        ordering = ['-timestamp']


# Model to track user behavior patterns
class UserBehavior(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    application_name = models.CharField(max_length=100, help_text="Name of the application in use")
    duration = models.DurationField(help_text="Duration of application usage")
    file_accessed = models.CharField(max_length=255, null=True, blank=True, help_text="Path to file accessed")
    keyboard_activity = models.IntegerField(help_text="Number of key presses")
    mouse_activity = models.IntegerField(help_text="Number of mouse clicks")

    def __str__(self):
        return f"User Behavior at {self.timestamp}"

    class Meta:
        verbose_name_plural = "User Behaviors"
        ordering = ['-timestamp']


# Model for data visualization and reporting preferences
class VisualizationPreference(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    graph_type = models.CharField(max_length=50, choices=[('line', 'Line'), ('bar', 'Bar'), ('pie', 'Pie')], help_text="Type of graph for data visualization")
    time_interval = models.DurationField(help_text="Time interval for data aggregation")
    display_historical_data = models.BooleanField(default=True, help_text="Whether to display historical data or not")

    def __str__(self):
        return f"Visualization Preference for {self.user.username}"

    class Meta:
        verbose_name_plural = "Visualization Preferences"
        ordering = ['user']


# Model for notifications and alerts
class NotificationAlert(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100, help_text="Type of alert, e.g., High CPU Usage, Unusual Network Activity")
    threshold_value = models.FloatField(help_text="Threshold value to trigger the alert")
    is_active = models.BooleanField(default=True, help_text="Whether the alert is currently active or not")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification Alert for {self.user.username} - {self.alert_type}"

    class Meta:
        verbose_name_plural = "Notification Alerts"
        ordering = ['-created_at']

