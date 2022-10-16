
from django.contrib.auth import get_user_model
from .models import BankAccount
from rest_framework import serializers

User = get_user_model()


class BankAccountSerializer(serializers.ModelSerializer):
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
        serializer = BankAccountSerializer(customer_account_query, many=True)

        return serializer.data
