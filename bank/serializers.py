from django.contrib.auth import get_user_model
from .models import BankAccount, History
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


class HistorySerializer(serializers.ModelSerializer):
    bank_account = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = '__all__'

    def get_client(self, obj):
        client_query = User.objects.get(
            first_name=obj)
        serializer = UserSerializer(client_query)

        return serializer.data['first_name']

    def get_bank_account(self, obj):

        client_query = User.objects.get(
            first_name=obj)
        customer_account_query = BankAccount.objects.get(
            client=client_query)
        serializer = BankAccountSerializer(customer_account_query)

        return serializer.data['account_number']
