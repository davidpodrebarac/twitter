from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ManyToManyField, DateField, DateTimeField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(_("Full Name"), blank=True, max_length=255)
    followers = ManyToManyField(
        "self",
        verbose_name="list of followers",
        related_name='follows',
        symmetrical=False,
    )

    def get_absolute_url(self):
        return reverse("users-detail", kwargs={"username": self.username})

    class Meta:
        ordering = ['date_joined']
