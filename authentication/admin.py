from django.contrib import admin
from .models import User, Otp
from booking.admin import OrderAdminInline, AddressInline

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'is_verified')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('full_name', 'phone_number')
    list_display_links = ('id', 'full_name')
    inlines = (OrderAdminInline, AddressInline)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'otp_code')
    list_filter = ('user', 'otp_code')
    list_display_links = ('id', 'user')
    search_fields = ('otp_code',)
    readonly_fields = ('user', 'otp_code', 'otp_key')