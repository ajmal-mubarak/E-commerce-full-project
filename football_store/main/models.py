from django.db import models


class ThemeSettings(models.Model):
    banner_bg = models.CharField(max_length=255, default="radial-gradient(#fff, #ffd6d6)")
    banner_heading = models.CharField(max_length=255, default="Give Your Workout A New Style!")
    banner_text = models.TextField(default="Success isn't always about greatness...")
    banner_image = models.ImageField(upload_to="theme/", blank=True, null=True)
    button_color = models.CharField(max_length=20, default="#ff523b")

    def __str__(self):
        return "Theme Settings"

    class Meta:
        verbose_name_plural = "Theme Settings"
