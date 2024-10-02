import requests
import allure
from endpoints.endpoint import Endpoint


class ExaminationToken(Endpoint):

    @allure.step('Проверка токена авторизации')
    def examination_token(self):

        # Выполняем запрос на проверку токена
        self.response = requests.get(
            f'{self.url_authorize}/{self.headers["Authorization"]}'
        )
        log = f"""
                    REQUEST:
                        URL: {self.response.request.url}
                        METHOD: {self.response.request.method}
                        HEADERS: {self.response.request.headers}

                    RESPONSE:
                        STATUS_CODE: {self.response.status_code}
                        CONTENT: {self.response.content}
                        TOKEN: {self.headers['Authorization']}
                    """
        print(log)

        # Проверка валидности токена по статусу ответа
        if self.response.status_code == 200:
            print(f"Токен валиден: {self.headers['Authorization']}")
            return True  # Токен валиден
        else:
            print(f"Токен невалиден: {self.headers['Authorization']}")
            return False  # Токен невалиден
