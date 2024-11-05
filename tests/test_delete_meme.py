import allure
import pytest


@allure.feature('Delete meme')
@allure.story('Implementation of memes')
@allure.title('Удаление мема')
@allure.description('Данный тест выполняет успешное удаление мема')
@pytest.mark.smoke
def test_delete_meme(examination_and_update_token, create_meme_fixture, delete_meme_endpoint, get_one_meme_endpoint):

    # Удаление мема
    delete_meme_endpoint.delete_meme(created_meme_id=create_meme_fixture)

    # Проверка статус кода ответа
    delete_meme_endpoint.check_that_status_is_200()

    # Проверка, что мем действительно удален
    delete_meme_endpoint.check_meme_deleted(meme_id=create_meme_fixture, get_one_meme_endpoint=get_one_meme_endpoint)


@allure.feature('Delete meme no identifier')
@allure.story('Implementation of memes')
@allure.title('Удаление мема без идентификатора')
@allure.description('Данный тест выполняет попытку удаление мема без указания идентификатора')
@pytest.mark.regression
@pytest.mark.regression_delete_meme
def test_delete_meme_no_identifier(examination_and_update_token, delete_meme_endpoint):

    # Удаление мема
    delete_meme_endpoint.delete_meme(created_meme_id=None)

    # Проверка статус кода ответа
    delete_meme_endpoint.check_that_status_is_404()


@allure.feature('Delete another user meme')
@allure.story('Implementation of memes')
@allure.title('Удаление мема другого пользователя')
@allure.description('Данный тест выполняет попытку удаление мема созданного другим пользователем')
@pytest.mark.regression
@pytest.mark.regression_delete_meme
def test_delete_another_user_meme(examination_and_update_token, get_meme_id_of_another_user, delete_meme_endpoint):

    # Удаление мема
    delete_meme_endpoint.delete_meme(created_meme_id=get_meme_id_of_another_user)

    # Проверка статус кода ответа
    delete_meme_endpoint.check_that_status_is_403()


@allure.feature('Delete meme without token')
@allure.story('Implementation of memes')
@allure.title('Удаление мема без токена')
@allure.description('Данный тест выполняет попытку удаление мема без указания токена в заголовки')
@pytest.mark.regression
@pytest.mark.regression_delete_meme
def test_delete_meme_without_token(
        examination_and_update_token, create_meme_and_restore_token_after_test,
        remove_token_from_headers, delete_meme_endpoint
):

    # Удаление мема
    delete_meme_endpoint.delete_meme(created_meme_id=create_meme_and_restore_token_after_test)

    # Проверка статус кода ответа
    delete_meme_endpoint.check_that_status_is_401()


@allure.feature('Delete meme with invalid token')
@allure.story('Implementation of memes')
@allure.title('Удаление мема с несуществующим токеном')
@allure.description('Данный тест выполняет попытку удаление мема с указанием не существующего токена в заголовок')
@pytest.mark.regression
@pytest.mark.regression_delete_meme
def test_delete_meme_with_invalid_token(
        examination_and_update_token, create_meme_and_restore_token_after_test,
        create_invalid_token, delete_meme_endpoint
):

    # Удаление мема
    delete_meme_endpoint.delete_meme(created_meme_id=create_meme_and_restore_token_after_test)

    # Проверка статус кода ответа
    delete_meme_endpoint.check_that_status_is_401()
