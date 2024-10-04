import allure
import pytest


@allure.feature('Getting all memes')
@allure.story('Implementation of memes')
@allure.title('Получение всех мемов')
@allure.description('Данный тест выполняет успешное получение всех мемов')
@pytest.mark.smoke
def test_getting_all_memes(examination_and_update_token, get_all_memes_endpoint):

    # Получение всех мемов
    get_all_memes_endpoint.getting_all_memes()

    # Проверка статус кода ответа
    get_all_memes_endpoint.check_that_status_is_200()

    # Проверка что в ответе содержится более 10 обьектов
    get_all_memes_endpoint.check_data_objects(min_objects=10)


@allure.feature('Getting all memes without token')
@allure.story('Implementation of memes')
@allure.title('Получение всех мемов без токена')
@allure.description('Данный тест выполняет попытку получения всех мемов без указания токена в заголовки')
@pytest.mark.negative
@pytest.mark.negative_getting_all_meme
def test_getting_all_memes_without_token(remove_token_from_headers, get_all_memes_endpoint):

    # Получение всех мемов
    get_all_memes_endpoint.getting_all_memes()

    # Проверка статус кода ответа
    get_all_memes_endpoint.check_that_status_is_401()


@allure.feature('Getting all memes with invalid token')
@allure.story('Implementation of memes')
@allure.title('Получение всех мемов с несуществующим токеном')
@allure.description(
    'Данный тест выполняет попытку получения всех мемов с указанием не существующего токена в заголовок'
)
@pytest.mark.negative
@pytest.mark.negative_getting_all_meme
def test_getting_all_memes_with_invalid_token(create_invalid_token, get_all_memes_endpoint):

    # Получение всех мемов
    get_all_memes_endpoint.getting_all_memes()

    # Проверка статус кода ответа
    get_all_memes_endpoint.check_that_status_is_401()
