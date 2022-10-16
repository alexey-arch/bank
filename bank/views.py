
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from .models import BankAccount
from .serializers import UserSerializer, BankAccountSerializer
from .utils import randomDigits

User = get_user_model()


class UserViewSet(GenericViewSet):
    @swagger_auto_schema(request_body=UserSerializer)
    @action(detail=False, methods=['post'])
    def get_users(self, request):
        queryset = User.objects.filter(**request.data)
        serializer_class = UserSerializer(queryset, context={
            'request': request,
        }, many=True)
        return Response(serializer_class.data)

    @swagger_auto_schema(request_body=UserSerializer)
    @action(detail=False, methods=['post'])
    def create_user(self, request, **kwargs):
        queryset = User.objects.create()
        return Response(status=status.HTTP_200_OK)


class AccountView(GenericViewSet):
    @swagger_auto_schema()
    @action(detail=False, methods=['post'])
    def create_account(self, request):
        data = {'client': request.user}
        account = BankAccount(client=data['client'],
                              account_number=f"KZ42722C{randomDigits(12)}",
                              amount='0',
                              currency='1',
                              card_number=f"4400{randomDigits(12)}",
                              status='1')
        account.save()

        queryset = BankAccount.objects.filter(**{'id': account.id})
        serializer_class = BankAccountSerializer(queryset, context={
            'request': request,
        }, many=True)
        if account:
            return Response(status=status.HTTP_200_OK, data=serializer_class.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=BankAccountSerializer)
    @action(detail=False, methods=['post'])
    def close_account(self, request):
        account = BankAccount.objects.filter(**request.data)
        for obj in account:
            obj.status = '2'
            obj.save()

        serializer_class = BankAccountSerializer(account, context={
            'request': request,
        }, many=True)

        if serializer_class:
            return Response(status=status.HTTP_200_OK, data=serializer_class.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=BankAccountSerializer)
    @action(detail=False, methods=['post'])
    def top_up_account(self, request):
        try:
            account = BankAccount.objects.filter(account_number=request.data['account_number'])
            for obj in account:
                if obj.status == '1':
                    amount = int(obj.amount)
                    amount += int(request.data['amount'])
                    obj.amount = amount
                    obj.save()
                else:
                    account = None

            serializer_class = BankAccountSerializer(account, context={
                'request': request,
            }, many=True)

            if account is None:
                return Response(status=status.HTTP_200_OK, data='Что-то пошло не так!')
            return Response(status=status.HTTP_200_OK, data=serializer_class.data)

        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=BankAccountSerializer)
    @action(detail=False, methods=['post'])
    def withdrawal_money(self, request):
        account = BankAccount.objects.filter(account_number=request.data['account_number'])
        for obj in account:
            if obj.status == '1':
                amount = int(obj.amount)
                amount -= int(request.data['amount'])
                obj.amount = amount
                obj.save()
            else:
                account = None

        serializer_class = BankAccountSerializer(account, context={
            'request': request,
        }, many=True)

        if account is None:
            return Response(status=status.HTTP_200_OK, data='Что-то пошло не так!')
        return Response(status=status.HTTP_200_OK, data=serializer_class.data)
