import allure
import copy
import random
from faker import Faker

fake = Faker()


class Endpoint:
    url = 'http://167.172.172.115:52355/meme'
    url_authorize = 'http://167.172.172.115:52355/authorize'
    token = None
    headers = {
        "Authorization": token
    }

    response = None
    json = None

    @staticmethod
    def random_type():
        """Генерация случайного типа данных (int, float, str)"""
        return random.choice([
            random.randint(0, 10),  # Случайное целое число
            round(random.uniform(0, 10), 2),  # Случайное число с плавающей точкой
            fake.word()  # Случайное слово (строка)
        ])

    @staticmethod
    def data_body(random_type):
        """Тело запроса с генерацией случайных данных"""
        return {
            "text": fake.company(),
            "url": "http://meme.ru",  # Исправленный формат URL
            "tags": [random_type() for _ in range(9)],  # Рандомные данные в поле tags
            "info": {f"key_{i}": random_type() for i in range(3)}  # Случайные данные
        }

    # Функция для создания вариаций с негативными данными
    def generate_invalid_data(self, field, invalid_value):
        """Генерирует JSON с заменой одного поля на невалидное значение."""
        data = copy.deepcopy(self.data_body(self.random_type))  # Используем копию, чтобы не изменить оригинал
        keys = field.split(".")
        obj = data
        for key in keys[:-1]:
            obj = obj.get(key, {})
        obj[keys[-1]] = invalid_value
        return data

    # Параметры для тестирования (поля и их невалидные значения)
    invalid_scenarios = [
        ("text", 12345),  # Неверный тип поля text
        ("text", None),  # Отсутствие обязательного поля text
        ("url", 123),  # Неверный формат URL
        ("url", None),  # Отсутствие обязательного поля url
        ("tags", "Super"),  # Неверный тип поля tags
        ("tags", None),  # Отсутствие обязательного поля tags
        ("info", "String"),  # Неверный тип поля info (строка вместо объекта)
        ("info", None)  # Отсутствие обязательного поля info
    ]

    @allure.step('Check that response is 200')
    def check_that_status_is_200(self):
        assert self.response.status_code == 200

    @allure.step('Check that response is 400')
    def check_that_status_is_400(self):
        assert self.response.status_code == 400

    @allure.step('Check that response is 401')
    def check_that_status_is_401(self):
        assert self.response.status_code == 401

    @allure.step('Check that response is 403')
    def check_that_status_is_403(self):
        assert self.response.status_code == 403

    @allure.step('Check that response is 404')
    def check_that_status_is_404(self):
        assert self.response.status_code == 404
