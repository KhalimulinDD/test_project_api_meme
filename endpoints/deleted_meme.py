import requests
import allure
from endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Delete meme')
    def delete_meme(self, created_meme_id):

        self.response = requests.delete(f"{self.url}/{created_meme_id}", headers=self.headers)

        # Если не передан created_meme_id, то указываем None.
        if created_meme_id is None:
            created_meme_id = None

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

    @allure.step('Checking for meme removal')
    def check_meme_deleted(self, meme_id, get_one_meme_endpoint):
        """Проверяет, что мем действительно удален, ожидая статус-код 404"""
        self.response = get_one_meme_endpoint.getting_one_meme(meme_id)
        assert self.response.status_code == 404
