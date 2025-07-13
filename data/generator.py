from faker import Faker
import allure
from datetime import datetime
import random
import string
import json


class TestGenerator:
    @staticmethod
    def generate_user():
        faker = Faker()
        email = faker.email()
        password = TestGenerator.generate_random_string(8)
        user = {
            "email": email,
            "password": password
        }
        return user


    @staticmethod
    def generate_uid():
        faker = Faker()
        uid = faker.uuid4()
        return uid

    @staticmethod
    def generate_time_now():
        now = datetime.now()
        return int(now.strftime("%H%M%S%d%m%Y"))

    @staticmethod
    def generate_random_string(length=8):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    @staticmethod
    def generate_amount() -> int:
        return random.randint(1, 1000)


    @staticmethod
    def create_listing_data():
        fake = Faker("ru_RU")  # Инициализация Faker для русского языка
        data = {
            'name': f'Объявление {TestGenerator.generate_random_string()}',  # Случайное слово
            'category': 'Хобби',
            'condition': 'Новый',
            'city': 'Москва',
            'description': 'Котёнок',
            'price': '1'
        }
        return data