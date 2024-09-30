import allure
import pytest
from endpoints.created_meme import CreateMeme


@allure.feature('Create meme')
@allure.story('Implementation of memes')
@allure.title('Создание мема')
@allure.description('Данный тест выполняет создание мема с валидными данными')
@pytest.mark.smoke
def test_create_meme(update_token, create_meme_endpoint, cleanup_meme_fixture, request):

    # Создание мема
    request.function.meme_id = create_meme_endpoint.create_new_meme()

    # Проверка созданного мема
    create_meme_endpoint.check_that_status_is_200()


@allure.feature('Create meme with incorrect_data')
@allure.story('Implementation of memes')
@allure.title('Создание мема с невалидными данными')
@allure.description(
    'Данный тест выполняет создание мема без указания обязательных полей или некорректным типом данных'
)
@pytest.mark.negative
@pytest.mark.parametrize('field, invalid_value', CreateMeme.invalid_scenarios)
def test_create_meme_incorrect_data(update_token, create_meme_endpoint, field, invalid_value):

    generator = CreateMeme()
    invalid_data = generator.generate_invalid_data(field, invalid_value)

    # Создание мема
    create_meme_endpoint.create_new_meme(invalid_data)

    # Проверка созданного мема
    create_meme_endpoint.check_that_status_is_400()


@allure.feature('Create meme without token')
@allure.story('Implementation of memes')
@allure.title('Создание мема без токена)')
@allure.description('Данный тест выполняет создание мема без указания токена в заголовок')
@pytest.mark.negative
def test_create_meme_without_token(remove_token_from_headers, create_meme_endpoint):

    # Создание мема
    create_meme_endpoint.create_new_meme()

    # Проверка созданного мема
    create_meme_endpoint.check_that_status_is_401()


@allure.feature('Create meme with invalid token')
@allure.story('Implementation of memes')
@allure.title('Создание мема с несуществующим токеном)')
@allure.description('Данный тест выполняет создание мема с указанием не существующего токена в заголовок')
@pytest.mark.negative
def test_create_meme_with_invalid_token(create_invalid_token, create_meme_endpoint):

    # Создание мема
    create_meme_endpoint.create_new_meme()

    # Проверка созданного мема
    create_meme_endpoint.check_that_status_is_401()
