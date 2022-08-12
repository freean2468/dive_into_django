from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField()
    nickname = models.CharField("Nickname", max_length=20)
    password = models.CharField("Password", max_length=24)
    name = models.CharField("Name", max_length=30)
    phone = models.CharField("Phone", max_length=20)

    def __str__(self):
        return self.email