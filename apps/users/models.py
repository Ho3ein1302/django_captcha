from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _

from .validators import check_phone


class User(AbstractUser):
    phone = models.CharField(db_index=True, unique=True, validators=[check_phone], verbose_name=_('phone'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
