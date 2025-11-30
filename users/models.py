from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = None
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name=_("Telefon raqami"),
        help_text=_("Telefon raqamingizni kiriting (masalan: +998901234567)")
    )
    is_student = models.BooleanField(
        default=True,
        verbose_name=_("Talaba"),
        help_text=_("Agar foydalanuvchi talaba bo'lsa, belgilang")
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)
