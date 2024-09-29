import requests
import allure
from endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Delete meme')
    def delete_meme(self, created_meme_id):
        self.response = requests.delete(f"{self.url}/{created_meme_id}", headers=self.headers)
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
        print(f"\nУдаление мема с ID: {created_meme_id}, Статус ответа: {self.response.status_code}")
        return self.response
