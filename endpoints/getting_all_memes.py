import requests
import allure
import random
from endpoints.endpoint import Endpoint


@allure.step('Получение всех мемов')
class GettingAllMemes(Endpoint):

    def getting_all_memes(self):

        self.response = requests.get(
            self.url,
            headers=self.headers
        )
        log = f"""
                    REQUEST:
                        URL: {self.response.request.url}
                        METHOD: {self.response.request.method}
                        HEADERS: {self.response.request.headers}

                    RESPONSE:    
                        STATUS_CODE: {self.response.status_code}
                    """
        print(log)

        # Проверяем, что ответ содержит JSON, прежде чем пытаться его декодировать
        try:
            self.json = self.response.json()
        except requests.exceptions.JSONDecodeError:
            print("Ошибка: ответ не содержит корректный JSON.")
            print("Ответ сервера:", self.response.text)
            return None

        return self.response

    def get_meme_ids_without_updated_by(self, excluded_user="KhalimulinDD", limit=10):
        """Метод для получения 10 id, где updated_by не равно excluded_user"""
        if not hasattr(self, 'json') or 'data' not in self.json:
            print("Ошибка: JSON не содержит ожидаемых данных.")
            return []

        # Фильтруем мемы по условию updated_by != 'KhalimulinDD'
        meme_ids = [
            meme['id'] for meme in self.json['data']
            if meme.get('updated_by') != excluded_user
        ]

        # Возвращаем не более 10 идентификаторов
        return meme_ids[:limit]

    def get_random_stranger_meme_id(self, excluded_user="KhalimulinDD"):
        """Получение случайного id для теста на удаление"""
        meme_ids = self.get_meme_ids_without_updated_by(excluded_user)

        if not meme_ids:
            print("Ошибка: не удалось получить идентификаторы мемов для удаления.")
            return None

        # Возвращаем случайный id
        return random.choice(meme_ids)

    def get_meme_ids_with_updated_by(self, excluded_user="KhalimulinDD", limit=10):
        """Метод для получения 10 id, где updated_by равно excluded_user"""
        if not hasattr(self, 'json') or 'data' not in self.json:
            print("Ошибка: JSON не содержит ожидаемых данных.")
            return []

        # Фильтруем мемы по условию updated_by = 'KhalimulinDD'
        meme_ids = [
            meme['id'] for meme in self.json['data']
            if meme.get('updated_by') == excluded_user
        ]

        # Возвращаем не более 10 идентификаторов
        return meme_ids[:limit]

    def get_random_meme_id(self, excluded_user="KhalimulinDD"):
        """Получение случайного id для теста на получение одного мема"""
        meme_ids = self.get_meme_ids_with_updated_by(excluded_user)

        if not meme_ids:
            print("Ошибка: не удалось получить идентификаторы мемов для удаления.")
            return None

        # Возвращаем случайный id
        return random.choice(meme_ids)

    def check_data_objects(self, min_objects):
        """Проверяет, что в массиве 'data' содержится более 10 объектов."""
        assert len(self.response.json()['data']) > min_objects
