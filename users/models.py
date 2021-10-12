from django.db import models
from core.models import TimeStamp


class User(TimeStamp):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    is_maker = models.BooleanField(default=False)
    agree_service = models.BooleanField(default=False)
    agree_maketing = models.BooleanField(default=False)

    class Meta:
        db_table = "users"
