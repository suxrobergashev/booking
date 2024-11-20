from django.urls import path

from .models import Address
from .views import OrderViewSet, MenuViewSet, AddressViewSet

urlpatterns = [
    path('menu/', MenuViewSet.as_view({'get': 'list', 'post': 'create'}), name='menu'),
    path('menu/<int:pk>/', MenuViewSet.as_view({'get': 'menu_detail', 'patch': "update"}), name='menu_detail'),
    path('address/', AddressViewSet.as_view({'get': 'list', 'post': 'create'}), name='address_list'),
    path('address/<int:pk>/', AddressViewSet.as_view({'patch': 'update'}), name='address_update'),
    path('orders/', OrderViewSet.as_view({'post': 'create', 'get': 'list'}), name='orders'),
    path('order/<int:pk>/', OrderViewSet.as_view({'get': 'order_detail'}), name='order_detail'),
]
