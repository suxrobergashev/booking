import requests
from django.conf import settings


def create_message(order):
    message = (f"User: {order.user.full_name} \nAddress:<a href='{order.address.url}'>"
               f"{order.address.address}</a>\nTotal price:{order.total_price}\n")
    for order_item in order.order_items.all():
        message += f"Product name {order_item.product.name}\nquantity {order_item.quantity}\n"
    return message


def send_notification(message: str) -> None:
    try:
        print(requests.get(settings.TELEGRAM_API_URL + message))
    except Exception as e:
        print(f"Failed while sending request to telegram client: {e}")
