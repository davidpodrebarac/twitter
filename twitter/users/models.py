from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ManyToManyField
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    full_name = models.CharField(_("Full Name"), blank=True, max_length=255)
    followers = ManyToManyField(
        "self",
        verbose_name="list of followers",
        related_name='follows',
        symmetrical=False,
    )

    class Meta:
        ordering = ['date_joined']
