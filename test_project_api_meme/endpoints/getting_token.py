import requests
import allure
import os
from endpoints.endpoint import Endpoint
from dotenv import load_dotenv

load_dotenv()


class GetToken(Endpoint):

    token = None

    @allure.step('Получение токена авторизации')
    def get_new_token(self):

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
        print(f'\nПолучение токена {self.response.json()}')
        self.json = self.response.json()
        self.token = self.json['token']
        return self.token
