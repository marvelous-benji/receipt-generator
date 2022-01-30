import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .usermanager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    fullname = models.CharField(_("fullname"), max_length=200, null=False)
    business_name = models.CharField(
        _("business name"), max_length=255, null=False, unique=True
    )
    business_address = models.CharField(
        _("business address"), max_length=200, null=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "business_name", "business_address"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
