import allure
import pytest
import os


@allure.feature('Getting token')
@allure.story('Implementation of token')
@allure.title('Получение токена')
@allure.description('Данный тест выполняет успешное получение токена')
@pytest.mark.smoke
def test_getting_token(get_token_endpoint):

    # Получаем логин
    login = os.getenv('LOGIN')

    # Получаем токен
    get_token_endpoint.get_new_token()

    # Проверка ответа
    get_token_endpoint.check_that_status_is_200()

    # Проверка user в ответе
    get_token_endpoint.check_response_user_is_correct(user=login)


@allure.feature('Getting token without name')
@allure.story('Implementation of token')
@allure.title('Получение токена без имени')
@allure.description('Данный тест выполняет попытку получения токена без указания имени пользователя в теле запроса')
@pytest.mark.negative
def test_getting_token_without_name(get_token_endpoint):

    # Получаем токен
    get_token_endpoint.get_new_token(payload={"name": None})

    # Проверка ответа
    get_token_endpoint.check_that_status_is_400()
