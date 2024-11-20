from uuid import uuid4

from django.db import models
from abstraction.base_model import BaseModel
from authentication.models import User

from django.db.models import F, Sum
from decimal import Decimal


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    url = models.URLField(blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.latitude is not None and self.longitude is not None:
            # Generate Google Maps URL with latitude and longitude
            self.url = f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        else:
            self.url = None  # Clear URL if latitude or longitude is missing
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.address}, {self.user}"


class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Menu(BaseModel):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu/')

    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.full_name

    def calculate_order(self):
        total = (self.order_items
                 .select_related('product')
                 .annotate(item_total=F('quantity') * F('product__price'))
                 .aggregate(order_total=Sum('item_total'))['order_total'] or Decimal('0.00'))

        self.total_price = total
        self.save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} {self.quantity}"
