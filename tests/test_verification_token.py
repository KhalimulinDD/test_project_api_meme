# import allure
# import pytest
#
#
# @allure.feature('Examination token')
# @allure.story('Implementation of token')
# @allure.title('Проверка токена')
# @allure.description('Данный тест выполняет успешную проверку токена на валидность')
# @pytest.mark.smoke
# def test_examination_token(update_token, exam_token_endpoint):
#
#     # Проверяем токен на валидность
#     exam_token_endpoint.examination_token()
#
#     # Проверка ответа
#     exam_token_endpoint.check_that_status_is_200()
#
#
# @allure.feature('Examination invalid token')
# @allure.story('Implementation of token')
# @allure.title('Проверка несуществующего токена')
# @allure.description('Данный тест выполняет проверку несуществующего токена')
# @pytest.mark.negative
# def test_examination_invalid_token(create_invalid_token, exam_token_endpoint):
#
#     # Проверяем токен на валидность
#     exam_token_endpoint.examination_token()
#
#     # Проверка ответа
#     exam_token_endpoint.check_that_status_is_404()
