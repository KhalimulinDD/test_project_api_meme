import requests
import allure
import os
from endpoints.endpoint import Endpoint
from dotenv import load_dotenv

load_dotenv()


class GetToken(Endpoint):

    token = None

    @allure.step('Получение токена авторизации')
    def get_new_token(self, payload=None):

        if payload is None:
            payload = {"name": os.getenv('LOGIN')}

        self.response = requests.post(
            self.url_authorize,
            json=payload
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

        # Проверяем, что ответ содержит JSON, прежде чем пытаться его декодировать
        try:
            self.json = self.response.json()
        except requests.exceptions.JSONDecodeError:
            print("Ошибка: ответ не содержит корректный JSON.")
            print("Ответ сервера:", self.response.text)
            return self.response

        self.token = self.json['token']

        return self.response

    @allure.step('Check that user is the same as sent')
    def check_response_user_is_correct(self, user):
        assert self.json['user'] == user
