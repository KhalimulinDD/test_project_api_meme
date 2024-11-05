import allure
import pytest
from endpoints.endpoint import Endpoint


@allure.feature('Create meme')
@allure.story('Implementation of memes')
@allure.title('Создание мема')
@allure.description('Данный тест выполняет создание мема с валидными данными')
@pytest.mark.smoke
def test_create_meme(examination_and_update_token, create_meme_endpoint, cleanup_meme_fixture, request):

    # Тело запроса
    create_body = {
        "text": "New meme",
        "url": "http//luk.ru",
        "tags": ["Super", 33, 44.3, True],
        "info": {
            "information": "Информация",
            "valid": "valid"
        }
    }

    # Создание мема
    request.function.meme_id = create_meme_endpoint.create_new_meme(payload=create_body)

    # Проверка статус кода ответа
    create_meme_endpoint.check_that_status_is_200()

    # Проверка значения во всех полях созданного мема
    create_meme_endpoint.check_meme_data_is_correct(create_body)


@allure.feature('Create meme with empty value or special characters')
@allure.story('Implementation of memes')
@allure.title('Создание мема с пустым значением или спецсимволами')
@allure.description(
    'Данный тест выполняет успешное создание мема с указанием пустой строки, массива, обьекта или спецсимволов'
)
@pytest.mark.regression
@pytest.mark.parametrize('field, valid_value', Endpoint.valid_scenarios)
def test_create_meme_correct_data(
        examination_and_update_token, create_meme_endpoint,
        cleanup_meme_fixture, field, valid_value, request, check_empty_field
):

    # Генерируем данные в теле запроса для теста
    generator = Endpoint()
    valid_data = generator.generate_valid_data(field, valid_value)

    # Создание мема
    request.function.meme_id = create_meme_endpoint.create_new_meme(valid_data)

    # Проверка статус кода ответа
    create_meme_endpoint.check_that_status_is_200()

    # Проверка, что поле содержит ожидаемое пустое значение
    check_empty_field(request.function.meme_id, field, valid_value)


@allure.feature('Create meme with incorrect_data')
@allure.story('Implementation of memes')
@allure.title('Создание мема с невалидными данными')
@allure.description(
    'Данный тест выполняет создание мема без указания обязательных полей или некорректным типом данных'
)
@pytest.mark.regression
@pytest.mark.regression_create_meme
@pytest.mark.parametrize('field, invalid_value', Endpoint.invalid_scenarios)
def test_create_meme_incorrect_data(examination_and_update_token, create_meme_endpoint, field, invalid_value):

    # Генерируем данные в теле запроса для теста
    generator = Endpoint()
    invalid_data = generator.generate_invalid_data(field, invalid_value)

    # Создание мема
    create_meme_endpoint.create_new_meme(invalid_data)

    # Проверка статус кода ответа
    create_meme_endpoint.check_that_status_is_400()


@allure.feature('Create meme without token')
@allure.story('Implementation of memes')
@allure.title('Создание мема без токена)')
@allure.description('Данный тест выполняет создание мема без указания токена в заголовок')
@pytest.mark.regression
@pytest.mark.regression_create_meme
def test_create_meme_without_token(remove_token_from_headers, create_meme_endpoint):

    # Создание мема
    create_meme_endpoint.create_new_meme()

    # Проверка статус кода ответа
    create_meme_endpoint.check_that_status_is_401()


@allure.feature('Create meme with invalid token')
@allure.story('Implementation of memes')
@allure.title('Создание мема с несуществующим токеном)')
@allure.description('Данный тест выполняет создание мема с указанием не существующего токена в заголовок')
@pytest.mark.regression
@pytest.mark.regression_create_meme
def test_create_meme_with_invalid_token(create_invalid_token, create_meme_endpoint):

    # Создание мема
    create_meme_endpoint.create_new_meme()

    # Проверка статус кода ответа
    create_meme_endpoint.check_that_status_is_401()
