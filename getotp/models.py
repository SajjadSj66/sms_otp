import random
import uuid
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db import models
import string


# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user

    @receiver(post_save, sender=User)
    def created_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.created(user=instance)

class OtpRequest(models.Model):
    class OtpChannel(models.TextChoices):
        ANDROID = 'Android', _('Android')
        IOS = 'IOS', _('iOS')
        WEB = 'Web', _('Web')

    request_id = models.UUIDField(default=uuid.uuid4, editable=False)
    channel = models.CharField(max_length=255,verbose_name=_("channel"), choices=OtpChannel.choices)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=4, null=True)
    valid_form = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now() + timedelta(seconds=500))
    receipt_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.channel

    def generate_password(self):
        self.password = self.random_password()
        self.valid_until = timezone.now() + timedelta(seconds=500)

    def random_password(self):
        rand = random.SystemRandom()
        digits = rand.choices(string.digits, k=5)
        return ''.join(digits)

    class Meta:
        verbose_name = _("One Time Password")
        verbose_name_plural = _("One Time Passwords")
