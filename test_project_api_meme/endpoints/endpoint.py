import allure


class Endpoint:
    url = 'http://167.172.172.115:52355/meme'
    url_authorize = 'http://167.172.172.115:52355/authorize'
    token = None
    headers = {
        "Authorization": token
    }

    response = None
    json = None

    # @allure.step('Check that title is the same as sent')
    # def check_response_title_is_correct(self, name):
    #     assert self.json['title'] == name

    @allure.step('Check that response is 200')
    def check_that_status_is_200(self):
        assert self.response.status_code == 200

    @allure.step('Check that response is 400')
    def check_that_status_is_400(self):
        assert self.response.status_code == 400

    @allure.step('Check that response is 401')
    def check_that_status_is_401(self):
        assert self.response.status_code == 401
