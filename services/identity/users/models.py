import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimestampedModel

from .managers import UserManager


class User(AbstractUser, TimestampedModel):
    username = None

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    email = models.EmailField(
        unique=True,
    )
    middle_name = models.CharField(
        max_length=150,
        blank=True,
    )
    phone = models.CharField(
        max_length=32,
        blank=True,
    )
    employee_id = models.UUIDField(
        null=True,
        blank=True,
    )
    is_verified = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["employee_id"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_verified"]),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return " ".join(
            part for part in [self.first_name, self.middle_name, self.last_name]
        ).strip()
