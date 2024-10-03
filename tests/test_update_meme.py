import allure
import pytest
from endpoints.endpoint import Endpoint


@allure.feature('Update your meme')
@allure.story('Implementation of memes')
@allure.title('Изменение своего мема')
@allure.description('Данный тест выполняет успешное изменение мема, созданного носителем токена из заголовка')
@pytest.mark.smoke
def test_update_your_meme(
        examination_and_update_token, create_meme_fixture, update_meme_endpoint, cleanup_meme_fixture, request
):
    update_body = {
        "id": create_meme_fixture,
        "text": "Good meme",
        "url": "http//luk.ru",
        "tags": ["Super", 33, 44.4],
        "info": {
            "information": "Тут не нужная информация"
        }
    }

    # Изменение мема
    request.function.meme_id = update_meme_endpoint.update_meme(meme_id=create_meme_fixture, payload=update_body)

    # Проверка созданного мема
    update_meme_endpoint.check_that_status_is_200()

    # Проверка значения в поле text измененного мема
    update_meme_endpoint.check_response_text_is_correct(update_body['text'])


@allure.feature('Update meme another user')
@allure.story('Implementation of memes')
@allure.title('Изменение мема другого пользователя')
@allure.description('Данный тест выполняет попытку изменения мема, созданного другим пользователем')
@pytest.mark.negative
def test_update_meme_another_user(
        examination_and_update_token, update_meme_endpoint, get_meme_id_of_another_user):

    update_body = {
        "id": get_meme_id_of_another_user,
        "text": "Good meme",
        "url": "http//luk.ru",
        "tags": ["Super", 33, 44.4],
        "info": {
            "information": "Тут не нужная информация"
        }
    }

    # Изменение мема
    update_meme_endpoint.update_meme(meme_id=get_meme_id_of_another_user, payload=update_body)

    # Проверка созданного мема
    update_meme_endpoint.check_that_status_is_403()


@allure.feature('Update meme with incorrect_data')
@allure.story('Implementation of memes')
@allure.title('Изменение мема с невалидными данными')
@allure.description(
    'Данный тест выполняет изменение мема без указания обязательных полей или некорректным типом данных'
)
@pytest.mark.negative
@pytest.mark.parametrize('field, invalid_value', Endpoint.invalid_scenarios)
def test_update_meme_incorrect_data(
        examination_and_update_token, create_meme_fixture,
        update_meme_endpoint, cleanup_meme_fixture, field, invalid_value, request
):

    # Сохраняем meme_id в request.function для удаления в cleanup
    request.function.meme_id = create_meme_fixture

    generator = Endpoint()
    invalid_data = generator.generate_invalid_data(field, invalid_value, meme_id=create_meme_fixture)

    # Создание мема
    update_meme_endpoint.update_meme(meme_id=create_meme_fixture, payload=invalid_data)

    # Проверка созданного мема
    update_meme_endpoint.check_that_status_is_400()


@allure.feature('Update meme without token')
@allure.story('Implementation of memes')
@allure.title('Изменение мема без токена')
@allure.description('Данный тест выполняет попытку изменения мема, без указания токена в заголовки')
@pytest.mark.negative
def test_update_meme_without_token(
        examination_and_update_token, create_and_update_meme_without_token, update_meme_endpoint
):

    # Вызов функции фикстуры с аргументом False для удаления токена
    meme_id, saved_token = create_and_update_meme_without_token

    update_body = {
        "id": meme_id,
        "text": "Good meme",
        "url": "http//luk.ru",
        "tags": ["Super", 33, 44.4],
        "info": {
            "information": "Тут не нужная информация"
        }
    }

    # Изменение мема
    update_meme_endpoint.update_meme(meme_id=meme_id, payload=update_body)

    # Проверка созданного мема
    update_meme_endpoint.check_that_status_is_401()


@allure.feature('Update meme invalid token')
@allure.story('Implementation of memes')
@allure.title('Изменение мема с несуществующим токеном')
@allure.description('Данный тест выполняет попытку изменения мема, с указанием несуществующего токена в заголовки')
@pytest.mark.negative
def test_update_meme_invalid_token(
        examination_and_update_token, create_and_update_meme_invalid_token, update_meme_endpoint
):

    # Вызов функции фикстуры с аргументом True для генерации не существующего токена
    meme_id, saved_token = create_and_update_meme_invalid_token

    update_body = {
        "id": meme_id,
        "text": "Good meme",
        "url": "http//luk.ru",
        "tags": ["Super", 33, 44.4],
        "info": {
            "information": "Тут не нужная информация"
        }
    }

    # Изменение мема
    update_meme_endpoint.update_meme(meme_id=meme_id, payload=update_body)

    # Проверка созданного мема
    update_meme_endpoint.check_that_status_is_401()
