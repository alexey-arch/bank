from django.contrib import admin

from .models import CustomUser, BankAccount, History

admin.site.register(CustomUser)
admin.site.register(BankAccount)
admin.site.register(History)

