import requests
import allure
import copy
import random
import numpy as np
from faker import Faker
from endpoints.endpoint import Endpoint

fake = Faker()


@allure.step('Создание мема')
class CreateMeme(Endpoint):
    meme_id = None

    def create_new_meme(self, payload=None):

        # Если не передан payload, генерируем случайные данные.
        if payload is None:
            payload = self.data_body()

        self.response = requests.post(
            self.url,
            json=payload,
            headers=self.headers
        )
        log = f"""
                    REQUEST:
                        URL: {self.response.request.url}
                        METHOD: {self.response.request.method}
                        JSON:   {self.response.request.body}
                        HEADERS: {self.response.request.headers}

                    RESPONSE:    
                        STATUS_CODE: {self.response.status_code}
                        CONTENT: {self.response.content}
                    """
        print(log)
        print(f'\nСоздание мема {self.response.json()}')
        self.json = self.response.json()
        self.meme_id = self.json['id']
        return self.meme_id

    @staticmethod
    def data_body():
        """Тело запроса с генерацией случайного названия для мема"""
        return {
            "text": fake.company(),
            "url": "http://meme.ru",  # Исправленный формат URL
            "tags": np.random.randint(0, 10, size=(9,)).tolist(),  # Одномерный массив
            "info": {f"key_{i}": random.randint(0, 100) for i in range(3)}  # Случайные данные
        }

    # Функция для создания вариаций с негативными данными
    def generate_invalid_data(self, field, invalid_value):
        """Генерирует JSON с заменой одного поля на невалидное значение."""
        data = copy.deepcopy(self.data_body())  # Используем глубокую копию, чтобы не изменить оригинал
        keys = field.split(".")  # Поддержка вложенных полей
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
