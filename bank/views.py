from django.shortcuts import render
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, status, generics

from .serializers import UserSerializer, CreateAccountSerializer, CloseAccountSerializer, \
    TopUpAccount

User = get_user_model()


class UserViewSet(GenericViewSet):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING)}
    ))
    @action(detail=False, methods=['post'])
    def get_users(self, request):
        queryset = User.objects.filter(**request.data)
        serializer_class = UserSerializer(queryset, context={
            'request': request,
        }, many=True)
        return Response(serializer_class.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['phone_number', 'iin', 'password', 'first_name', 'last_name', 'middle_name', 'is_staff',
                  'is_superuser', 'registration_date', 'account', 'is_active', 'is_staff', 'is_superuser', 'is_active'],
        properties={
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'middle_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'iin': openapi.Schema(type=openapi.TYPE_STRING),
            'account': openapi.Schema(type=openapi.TYPE_STRING),
            'registration_date': openapi.Schema(type=openapi.TYPE_STRING),
            'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }))
    @action(detail=False, methods=['post'])
    def create_user(self, request, **kwargs):
        queryset = User.objects.create()
        return Response(status=status.HTTP_200_OK)


class AccountView(GenericViewSet):
    @swagger_auto_schema()
    @action(detail=False, methods=['post'])
    def create_account(self, request):
        data = {'client': request.user}
        serializer_class = CreateAccountSerializer().create_bank_account(data=data)
        if serializer_class:
            return Response(status=status.HTTP_200_OK, data=serializer_class.values())
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING)}
    ))
    @action(detail=False, methods=['post'])
    def close_account(self, request):
        serializer_class = CloseAccountSerializer().close_bank_account(request.data)
        if serializer_class:
            return Response(status=status.HTTP_200_OK, data=serializer_class.values())
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['account_number', 'amount'],
        properties={
            'account_number': openapi.Schema(type=openapi.TYPE_STRING),
            'amount': openapi.Schema(type=openapi.TYPE_STRING)
        }))
    @action(detail=False, methods=['post'])
    def top_up_account(self, request):
        try:
            serializer_class = TopUpAccount().top_up(request.data)
            if serializer_class is None:
                return Response(status=status.HTTP_200_OK, data='Что-то пошло не так!')
            return Response(status=status.HTTP_200_OK, data=serializer_class.values())

        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['account_number', 'amount'],
        properties={
            'account_number': openapi.Schema(type=openapi.TYPE_STRING),
            'amount': openapi.Schema(type=openapi.TYPE_STRING)
        }))
    @action(detail=False, methods=['post'])
    def withdrawal_money(self, request):
        pass
