import copy
import allure
import random
import pytest
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
    def generate_invalid_data(self, field, invalid_value, meme_id=None):
        """Генерирует JSON с заменой одного поля на невалидное значение."""
        data = copy.deepcopy(self.data_body(self.random_type))  # Используем копию, чтобы не изменить оригинал

        # Добавляем поле id, если meme_id передан (для теста на изменение)
        if meme_id is not None:
            data['id'] = meme_id

        keys = field.split(".")
        obj = data
        for key in keys[:-1]:
            obj = obj.get(key, {})
        obj[keys[-1]] = invalid_value
        return data

    # Параметры для тестирования (поля и их невалидные значения)
    invalid_scenarios = [

        # Поле text с типом (String)
        ("text", 12345),  # Int вместо String
        ("text", 1234.5),  # Float вместо String
        ("text", None),  # Пустое значение
        ("text", ["Array", "Instead", "Of", "String"]),  # Array вместо String
        ("text", {"object": "instead of string"}),  # Object вместо String

        # Поле url с типом (String)
        ("url", 123),  # Int вместо String
        ("url", 123.2),  # # Float вместо String
        ("url", None),  # Пустое значение
        ("url", ["http://array.com", "http://instead.com"]),  # Array вместо String
        ("url", {"object": "instead of URL"}),  # Object вместо String

        # Поле tags с типом (Array)
        ("tags", 12345),  # Int вместо Array
        ("tags", 1234.5),  # Float вместо Array
        ("tags", None),  # Пустое значение
        ("tags", "Super"),  # String вместо Array
        pytest.param(
            "tags", [None], marks=pytest.mark.xfail(
                reason="Ожидаемый фейл из-за бага с пустым значением тега"
            )
        ),  # Значение None в тэге
        ("tags", {"object": "instead of array"}),  # Object вместо Array

        # Поле info с типом (Object)
        ("info", 12345),  # Int вместо Object
        ("info", 1234.5),  # Float вместо Object
        ("info", None),  # Пустое значение
        ("info", "String"),  # String вместо Object
        ("info", ["Array", "Instead", "Of", "Object"]),  # Array вместо Object
    ]

    # Функция для создания вариаций с пустыми строками, массивами и обьектами
    def generate_valid_data(self, field, valid_value):
        """Генерирует JSON с заменой одного поля на пустую строку,массив или обьект"""
        data = copy.deepcopy(self.data_body(self.random_type))  # Используем копию, чтобы не изменить оригинал
        keys = field.split(".")
        obj = data
        for key in keys[:-1]:
            obj = obj.get(key, {})
        obj[keys[-1]] = valid_value
        return data

    # Параметры для тестирования (поля и пустые строки, массивы, обьекты и спецсимволы)
    valid_scenarios = [

        # Поле text
        ("text", ""),  # Пустая строка
        ("text", "!#$%^&*()_+"),  # Спецсимволы

        # Поле url
        ("url", ""),  # Пустая строка
        ("url", "!#$%^&*()_+"),  # Спецсимволы

        # Поле tags
        ("tags", []),  # Пустой массив
        ("tags", ["!#$%^&*()_+"]),  # Спецсимволы в массиве

        # Поле info
        ("info", {}),  # Пустой обьект
        ("info", {"special_characters": "!#$%^&*()_+"}),  # Спецсимволы в обьекте
    ]

    @allure.step('Checking the response body')
    def check_meme_data_is_correct(self, expected_data):
        """Проверяет, что все данные в ответе соответствуют ожидаемым данным."""
        for key, expected_value in expected_data.items():

            if key == "id":
                continue

            assert key in self.json
            actual_value = self.json[key]

            if isinstance(expected_value, dict):
                # Если значение — словарь (например, "info"), проверяем рекурсивно
                assert isinstance(actual_value, dict)
                for sub_key, sub_value in expected_value.items():
                    assert sub_key in actual_value
                    assert actual_value[sub_key] == sub_value
            else:
                # Проверка остальных типов данных (строки, числа, списки и т.д.)
                assert actual_value == expected_value

        print("Все поля успешно проверены.")

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
