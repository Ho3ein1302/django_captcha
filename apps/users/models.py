from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _

from .validators import check_phone


class Users(AbstractUser):
    phone = models.CharField(db_index=True, unique=True, validators=[check_phone], verbose_name=_('phone'))

    def clean(self):
        self.password = make_password(self.password)
        super().clean()
