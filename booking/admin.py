from django.contrib import admin
from .models import Menu, Address, Order, OrderItem, Tag


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdminInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'tags__name')
    list_editable = ('is_active',)
    list_display_links = ('id', 'name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address',)
    list_filter = ('user', 'address', 'created_at')
    list_display_links = ('id', 'user', 'address',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'address')
    list_filter = ('user', 'total_price', 'created_at')
    list_display_links = ('id', 'user', 'total_price')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity')
    list_filter = ('product', 'quantity', 'created_at')
    list_display_links = ('id', 'product',)
    list_editable = ('quantity',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name', 'created_at')
    list_display_links = ('id', 'name')
