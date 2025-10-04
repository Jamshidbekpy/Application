from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class Role(models.TextChoices):
    USER = "USER", _("User")
    ADMIN = "ADMIN", _("Admin")


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(_("role"), max_length=20, choices=Role.choices, default=Role.USER)
    bio = models.TextField(_("biography"), blank=True, null=True)
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
