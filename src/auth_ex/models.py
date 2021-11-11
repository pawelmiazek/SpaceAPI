from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from cores.models import Core


class User(AbstractUser):
    core = models.ForeignKey(
        Core,
        related_name="users",
        verbose_name=_("core"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
