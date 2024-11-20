from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from .models import Menu, Address, Order
from .serializers import MenuSerializer, ResponseMenuSerializer, OrderSerializer, OrderItemSerializer, \
    AddressSerializer, ResponseAddressSerializer, CreateOrderSerializer, ResponseOrderSerializer
from .utils import send_notification, create_message


class MenuViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create a menu',
        responses={201: ResponseMenuSerializer()},
        request_body=MenuSerializer(),
        tags=['Menu'],
    )
    def create(self, request):
        data = request.data
        serializer = MenuSerializer(data=data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(
            {'result': ResponseMenuSerializer(serializer.data, context={'request': request}).data, 'ok': True},
            status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Menu list',
        responses={200: ResponseMenuSerializer(many=True)},
        manual_parameters=[openapi.Parameter(name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                             description="search by product name or tag name")],
        tags=['Menu'],
    )
    def list(self, request):
        q = request.GET.get('q', None)
        menus = Menu.objects.filter((Q(name__icontains=q) | Q(tags__name__icontains=q)), is_active=True)
        return Response(
            {"result": ResponseMenuSerializer(menus, many=True, context={'request': request}).data, 'ok': True},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update a menu',
        tags=['Menu'],
    )
    def update(self, request, pk=None):
        data = request.data
        menu = Menu.objects.filter(pk=pk).first()
        serializer = MenuSerializer(menu, data=data, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(
            {'result': ResponseMenuSerializer(serializer.data, context={'request': request}).data, 'ok': True},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail a menu',
        responses={200: ResponseMenuSerializer()},
        tags=['Menu'],
    )
    def menu_detail(self, request, pk=None):
        menu = Menu.objects.filter(pk=pk).first()
        if not menu:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        return Response({'result': ResponseMenuSerializer(menu, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_200_OK)


class AddressViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create a address',
        responses={201: ResponseAddressSerializer()},
        request_body=AddressSerializer(),
        tags=['Address'],
    )
    def create(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = AddressSerializer(data=data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(
            {'result': ResponseAddressSerializer(serializer.data, context={'request': request}).data, 'ok': True},
            status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='User address list',
        responses={200: ResponseAddressSerializer(many=True)},
        tags=['Address'],
    )
    def list(self, request):
        addresses = Address.objects.filter(user_id=request.user.id)
        return Response(
            {"result": ResponseAddressSerializer(addresses, many=True, context={'request': request}).data, "ok": True},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update a address',
        responses={200: ResponseAddressSerializer()},
        request_body=AddressSerializer(),
        tags=['Address'],
    )
    def update(self, request, pk=None):
        data = request.data
        address = Address.objects.filter(id=pk, user_id=request.user.id).first()
        if not address:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = AddressSerializer(address, data=data, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(
            {'result': ResponseAddressSerializer(serializer.data, context={'request': request}).data, 'ok': True}, )


class OrderViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=CreateOrderSerializer(),
        responses={201: ResponseOrderSerializer()},
        tags=['Order'],
    )
    def create(self, request):
        data = request.data
        serializer = CreateOrderSerializer(data=data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        order_data = {
            'user': request.user.id,  # Assumes authenticated user
            'address': data.get('address')
        }
        order_create = OrderSerializer(data=order_data)
        if not order_create.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=order_create.errors)
        order = order_create.save()
        for item in data.get('order_items', []):
            item['order'] = order.id
            serializer = OrderItemSerializer(data=item)
            if not serializer.is_valid():
                order.delete()
                raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
            serializer.save()
        order.calculate_order()
        message = create_message(order)
        send_notification(message)
        return Response({'result': ResponseOrderSerializer(order, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='order List',
        responses={200: ResponseOrderSerializer(many=True)},
        tags=['Order'],
    )
    def list(self, request):
        orders = Order.objects.filter(user_id=request.user.id)
        serializer = ResponseOrderSerializer(orders, many=True, context={'request': request}).data
        return Response({'result': serializer, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='order Detail',
        responses={200: ResponseOrderSerializer()},
        tags=['Order'],
    )
    def order_detail(self, request, pk=None):
        order = Order.objects.filter(id=pk, user=request.user.id).first()
        if not order:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = ResponseOrderSerializer(order, context={'request': request}).data
        return Response({'result': serializer, 'ok': True}, status=status.HTTP_200_OK)
