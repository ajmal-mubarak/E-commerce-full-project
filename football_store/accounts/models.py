from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone  # ✅ import timezone

class EmailOTP(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    # OTP expiry 5 minutes
    OTP_EXPIRY_MINUTES = 5

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=self.OTP_EXPIRY_MINUTES)