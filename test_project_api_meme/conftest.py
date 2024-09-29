import pytest
from endpoints.getting_token import GetToken
from endpoints.verification_token import ExaminationToken
from endpoints.created_meme import CreateMeme
from endpoints.deleted_meme import DeleteMeme
from endpoints.endpoint import Endpoint


@pytest.fixture()
def get_token():
    return GetToken()


@pytest.fixture()
def exam_token():
    return ExaminationToken


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture()
def update_token(get_token, exam_token):
    """Фикстура для проверки и обновления токена перед выполнением теста."""
    # Проверка существующего токена
    if Endpoint.headers.get("Authorization"):
        # Создаем экземпляр ExaminationToken для проверки токена
        exam_instance = exam_token()

        # Проверяем валидность текущего токена
        is_valid = exam_instance.examination_token()

        if is_valid:
            print(f"Токен валиден: {Endpoint.headers['Authorization']}")
            return  # Токен валиден, выходим из фикстуры

    # Если токен не существует или не валиден, получаем новый токен
    print("Токен отсутствует или не валиден. Получаем новый токен...")
    token = get_token.get_new_token()

    # Обновляем токен в заголовках класса Endpoint
    Endpoint.token = token
    Endpoint.headers['Authorization'] = token

    print(f"Токен обновлен в заголовках: {Endpoint.headers['Authorization']}")


@pytest.fixture()
def cleanup_meme_fixture(request):
    """Фикстура для удаления продукта после выполнения теста."""
    yield
    meme_id = request.function.meme_id
    delete_meme = DeleteMeme()
    delete_meme.delete_meme(created_meme_id=meme_id)
