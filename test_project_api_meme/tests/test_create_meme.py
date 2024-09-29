import allure
import pytest
from endpoints.created_meme import CreateMeme


# @allure.story('Implementation of memes')
# @allure.title('Создание мема')
# @allure.description('Данный тест выполняет создание мема с валидными данными')
# @pytest.mark.smoke
# def test_create_meme(update_token, create_meme_endpoint, cleanup_meme_fixture, request):
#
#     # Создание продукта
#     request.function.meme_id = create_meme_endpoint.create_new_meme()
#
#     # Проверка созданного продукта
#     create_meme_endpoint.check_that_status_is_200()


@allure.story('Implementation of memes')
@allure.title('Создание мема (Негативный сценарий)')
@allure.description('Данный тест выполняет создание мема с невалидными данными')
@pytest.mark.smoke
@pytest.mark.parametrize('field, invalid_value', CreateMeme.invalid_scenarios)
def test_create_meme_negative(update_token, create_meme_endpoint, request, field, invalid_value):

    generator = CreateMeme()
    invalid_data = generator.generate_invalid_data(field, invalid_value)

    # Создание продукта
    create_meme_endpoint.create_new_meme(invalid_data)

    # # Проверка созданного продукта
    # create_meme_endpoint.check_that_status_is_400()
