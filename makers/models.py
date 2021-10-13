from django.db import models
from core.models import TimeStamp


class Maker(TimeStamp):
    makername = models.CharField(max_length=40)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    makernickname = models.CharField(max_length=40)
    profile = models.ImageField(null=True, blank=True, upload_to="profile/")
    introduce = models.TextField()
    idcard = models.ImageField(null=True, blank=True, upload_to="idcard/")
    bankbook_image = models.ImageField(null=True, blank=True, upload_to="bankbook/")
    status = models.CharField(max_length=40)
    bank = models.CharField(max_length=45)
    account_number = models.IntegerField(null=True, blank=True)
    account_holder = models.CharField(max_length=45)
    productform = models.CharField(max_length=45)
    language = models.ManyToManyField("Language", blank=True)
    region = models.ManyToManyField("Region", blank=True)
    category = models.ManyToManyField("Category", blank=True)
    tour = models.ManyToManyField("Tour", through="Maker_tour", blank=True)
    have_car = models.BooleanField(default=False)
    passenger_limit = models.IntegerField(null=True, blank=True)
    available_schedule = models.ManyToManyField("Available_schedule", blank=True)
    available_service = models.ManyToManyField("Available_service", blank=True)

    class Meta:
        db_table = "makers"


class Sns(models.Model):
    kind = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    maker = models.ForeignKey("Maker", on_delete=models.CASCADE)

    class Meta:
        db_table = "sns"


class Evidence(models.Model):
    kind = models.CharField(max_length=45)
<<<<<<< HEAD
    image = models.ImageField(upload_to="evidence")
=======
    image = models.ImageField(upload_to="evidence/")
>>>>>>> 4e8073bcfba104b2e9e41ee960e2a3de0b9ff833
    maker = models.ForeignKey("Maker", on_delete=models.CASCADE)

    class Meta:
        db_table = "evidences"


class Language(models.Model):
    Language = models.CharField(max_length=45)

    class Meta:
        db_table = "languages"


class Region(models.Model):
    region = models.CharField(max_length=45)

    class Meta:
        db_table = "regions"


class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "categories"


class Tour(models.Model):
    kind = models.CharField(max_length=45)

    class Meta:
        db_table = "tours"


class Maker_tour(models.Model):
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE)
    maker = models.ForeignKey("Maker", on_delete=models.CASCADE)
    limit_people = models.IntegerField()
    limit_load = models.IntegerField()

    class Meta:
        db_table = "maker_tours"


class Contact_channel(models.Model):
    kind = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    maker = models.ForeignKey("Maker", on_delete=models.CASCADE)

    class Meta:
        db_table = "contact_channels"


class Available_schedule(models.Model):
    schedule = models.CharField(max_length=45)

    class Meta:
        db_table = "available_schdules"


class Available_service(models.Model):
    service = models.CharField(max_length=45)

    class Meta:
        db_table = "available_services"
