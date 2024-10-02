import requests
import allure
import random
from endpoints.endpoint import Endpoint


@allure.step('Получение одного мема')
class GettingOneMeme(Endpoint):

    def getting_one_meme(self, meme_id=None):

        # Если не передан meme_id, генерируем случайные данные.
        if meme_id is None:
            meme_id = random.randint(1, 100)

        self.response = requests.get(
            f'{self.url}/{meme_id}',
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
