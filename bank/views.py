from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.schemas import openapi
from drf_yasg import openapi
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import status

from .models import BankAccount, History
from .serializers import UserSerializer, BankAccountSerializer, HistorySerializer
from .utils import randomDigits

User = get_user_model()


class UserViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountView(ViewSet):
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
        serializer_class = BankAccountSerializer(account, context={
            'request': request,
        })
        if account:
            return Response(status=status.HTTP_200_OK, data=serializer_class.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['account'],
        properties={'account_number': openapi.Schema(type=openapi.TYPE_STRING)}))
    @action(detail=False, methods=['post'])
    def close_account(self, request):
        account = BankAccount.objects.get(**request.data)
        account.status = '2'
        account.save()

        serializer_class = BankAccountSerializer(account, context={
            'request': request,
        })

        if serializer_class:
            return Response(status=status.HTTP_200_OK, data=serializer_class.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['account', 'amount'],
        properties={
            'account_number': openapi.Schema(type=openapi.TYPE_STRING),
            'amount': openapi.Schema(type=openapi.TYPE_STRING)}))
    @action(detail=False, methods=['post'])
    def top_up_account(self, request):
        try:
            account = BankAccount.objects.get(account_number=request.data['account_number'])

            if account.status == '1':
                amount = int(account.amount)
                amount += int(request.data['amount'])
                account.amount = amount
                account.save()
            else:
                account = None

            serializer_class = BankAccountSerializer(account, context={
                'request': request,
            })

            if account is None:
                return Response(status=status.HTTP_200_OK, data='Что-то пошло не так!')
            return Response(status=status.HTTP_200_OK, data=serializer_class.data)

        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['account', 'amount'],
        properties={
            'account': openapi.Schema(type=openapi.TYPE_STRING),
            'amount': openapi.Schema(type=openapi.TYPE_STRING)}))
    @action(detail=False, methods=['post'])
    def withdrawal_money(self, request):
        account = BankAccount.objects.get(account_number=request.data['account'])
        if account.status == '1':
            amount = int(account.amount)
            if amount < int(request.data['amount']):
                return Response(status=status.HTTP_200_OK, data='Недостаточно средств!')
            if int(request.data['amount']) < 100:
                return Response(status=status.HTTP_200_OK, data='Минимальная сумма перевода 100!')
            amount -= int(request.data['amount'])
            account.amount = amount
            account.save()
        else:
            account = None

        serializer_class = BankAccountSerializer(account, context={
            'request': request,
        })

        if account is None:
            return Response(status=status.HTTP_200_OK, data='Что-то пошло не так!')
        return Response(status=status.HTTP_200_OK, data=serializer_class.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['account', 'recipient', 'amount'],
        properties={
            'account': openapi.Schema(type=openapi.TYPE_STRING),
            'recipient': openapi.Schema(type=openapi.TYPE_STRING),
            'amount': openapi.Schema(type=openapi.TYPE_STRING)}))
    @action(detail=False, methods=['post'])
    def transaction(self, request):
        account = BankAccount.objects.get(account_number=request.data['account'])
        recipient = BankAccount.objects.get(account_number=request.data['recipient'])

        if account.status != '1':
            return Response(status=status.HTTP_200_OK, data='счет не активен!')
        amount = int(account.amount)
        if int(request.data['amount']) > amount:
            return Response(status=status.HTTP_200_OK, data='Недостаточно средств!')
        amount -= int(request.data['amount'])
        account.amount = amount
        account.save()

        if recipient.status != '1':
            return Response(status=status.HTTP_200_OK, data='счет получателя не активен!')
        amount = int(recipient.amount)
        amount += int(request.data['amount'])
        recipient.amount = amount
        recipient.save()

        data = {"client": recipient.client,
                "amount": request.data['amount'],
                "bank_account": account,
                "data_time": datetime.now()}

        History.objects.create(**data)

        serializer_class = BankAccountSerializer(recipient, context={
            'request': request,
        })
        print(recipient)
        return Response(status=status.HTTP_200_OK, data=serializer_class.data)


class HistoryView(ViewSet):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['account'],
        properties={'account': openapi.Schema(type=openapi.TYPE_STRING)}))
    @action(detail=False, methods=['post'])
    def get_history(self, request):
        account = BankAccount.objects.get(account_number=request.data['account'])
        queryset = History.objects.filter(bank_account=account)

        serializer_class = HistorySerializer(queryset, context={
            'request': request,
        }, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer_class.data)
