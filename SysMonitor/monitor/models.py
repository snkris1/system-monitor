from django.db import models

class InputActivity(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    keyboard_activity = models.PositiveIntegerField(help_text="Number of key presses")
    mouse_activity = models.PositiveIntegerField(help_text="Number of mouse clicks")

    def __str__(self):
        return f"Input Activity at {self.timestamp}"

    class Meta:
        verbose_name_plural = "Input Activities"
        ordering = ['-timestamp']
