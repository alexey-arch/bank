from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """
    Пользовательский менеджер моделей пользователей,
    где электронная почта является уникальным идентификатором
    для аутентификации вместо имен пользователей.
    """

    def create_user(self, phone_number, password, **extra_fields):
        # if not email:
        #     raise ValueError(_('Users must have an email address'))

        user = self.model(phone_number=phone_number, **extra_fields)
        iin = self.model()

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone_number, password, **extra_fields)
