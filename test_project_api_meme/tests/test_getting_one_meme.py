import allure
import pytest


@allure.feature('Getting one your meme')
@allure.story('Implementation of memes')
@allure.title('Получение своего мема')
@allure.description('Данный тест выполняет успешное получение мема, созданного носителем токена из заголовка')
@pytest.mark.smoke
def test_getting_one_your_meme(examination_and_update_token, getting_your_meme_id, get_one_meme_endpoint):

    # Получаем один мем созданый носителем токена в заголовке
    get_one_meme_endpoint.getting_one_meme(meme_id=getting_your_meme_id)

    # Проверка ответа
    get_one_meme_endpoint.check_that_status_is_200()


@allure.feature('Getting one meme another user')
@allure.story('Implementation of memes')
@allure.title('Получение мема чужого пользователя')
@allure.description('Данный тест выполняет успешное получение мема, созданного другим пользователем')
@pytest.mark.smoke
def test_getting_one_another_meme(examination_and_update_token, get_meme_id_of_another_user, get_one_meme_endpoint):

    # Получаем один мем созданый другим пользователем
    get_one_meme_endpoint.getting_one_meme(meme_id=get_meme_id_of_another_user)

    # Проверка ответа
    get_one_meme_endpoint.check_that_status_is_200()


@allure.feature('Getting one meme without token')
@allure.story('Implementation of memes')
@allure.title('Получение одного мема без токена')
@allure.description('Данный тест выполняет попытку получения одного мема без указания токена в заголовки')
@pytest.mark.negative
def test_getting_one_meme_without_token(remove_token_from_headers, get_one_meme_endpoint):

    # Получаем один мем
    get_one_meme_endpoint.getting_one_meme()

    # Проверка ответа
    get_one_meme_endpoint.check_that_status_is_401()


@allure.feature('Getting one meme with invalid token')
@allure.story('Implementation of memes')
@allure.title('Получение одного мема с несуществующим токеном')
@allure.description('Данный тест выполняет попытку получения одного мема без указания токена в заголовки')
@pytest.mark.negative
def test_getting_one_meme_with_invalid_token(create_invalid_token, get_one_meme_endpoint):

    # Получаем один мем
    get_one_meme_endpoint.getting_one_meme()

    # Проверка ответа
    get_one_meme_endpoint.check_that_status_is_401()
