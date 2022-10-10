from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    phone_number = models.CharField(max_length=10, unique=True, null=False)
    iin = models.CharField(max_length=12, null=False)
    password = models.CharField(max_length=250, null=False)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250)
    is_staff = models.BooleanField(null=False)
    is_superuser = models.BooleanField(null=False)
    is_active = models.BooleanField(null=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('iin',)

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class BankAccount(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    amount = models.CharField(max_length=500)
    currency = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    status = models.CharField(max_length=1)

    def __str__(self):
        return self.account_number

