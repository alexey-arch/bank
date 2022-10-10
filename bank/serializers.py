import random
from django.contrib.auth import get_user_model

from .exeption import Error
from .models import BankAccount
from rest_framework import serializers

User = get_user_model()


class Bank_accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    accounts_items = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_accounts_items(self, obj):
        customer_account_query = BankAccount.objects.filter(
            client=obj.id)
        serializer = Bank_accountSerializer(customer_account_query, many=True)

        return serializer.data


def randomDigits(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    return random.randint(lower, upper)


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

    def create_bank_account(self, data):
        account = BankAccount(client=data['client'],
                              account_number=f"KZ42722C{randomDigits(12)}",
                              amount='0',
                              currency='1',
                              card_number=f"4400{randomDigits(12)}",
                              status='1')
        account.save()
        return account


class CloseAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

    def close_bank_account(self, data):
        account = BankAccount.objects.filter(**data)
        for obj in account:
            obj.status = '2'
            obj.save()
        return account


class TopUpAccount(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

    def top_up(self, data):
        account = BankAccount.objects.filter(account_number=data['account_number'])
        for obj in account:
            if obj.status == '1':
                amount = int(obj.amount)
                amount += int(data['amount'])
                obj.amount = amount
                obj.save()
            else:
                return None
        return account


class WithdrawalMoneyAccount(serializers.ModelSerializer):
    def withdrawal_money(self, data):
        account = BankAccount.objects.filter(account_number=data['account_number'])
        for obj in account:
            pass
