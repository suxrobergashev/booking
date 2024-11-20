# Django Booking Loyihasini Ishga Tushirish Qo'llanmasi

## Talablar
- Python 3.9 yoki undan yuqori
- Git
- Virtual environment uchun `venv` yoki `virtualenv`
- PostgreSQL (yoki siz ishlatmoqchi bo'lgan boshqa DB)

## O'rnatish

1. Loyihani klonlash:
    ```bash
    git clone (https://github.com/suxrobergashev/booking.git)
    cd booking
    ```

2. Virtual environment yaratish:
    ```bash
    python -m venv venv
    source venv/bin/activate # Windows uchun: venv\Scripts\activate
    ```

3. Zarur kutubxonalarni o'rnatish:
    ```bash
    pip install -r requirements.txt
    ```

4. `.env` faylini sozlash:
   `.env.example` faylidan nusxa olib `.env` deb nomlang va kerakli ma'lumotlarni kiriting.

5. Ma'lumotlar bazasini sozlash:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Superuser yaratish:
    ```bash
    python manage.py createsuperuser
    ```

7. Loyihani ishga tushirish:
    ```bash
    python manage.py runserver
    ```

## Telegram Bot Xabar Yuborish
Loyiha ichida `.env` faylga Telegram bot tokeni va chat ID'ni kiriting:
