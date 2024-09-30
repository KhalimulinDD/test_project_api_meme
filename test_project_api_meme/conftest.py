import pytest
import random
import string
from endpoints.endpoint import Endpoint
from endpoints.getting_token import GetToken
from endpoints.created_meme import CreateMeme
from endpoints.deleted_meme import DeleteMeme
from endpoints.getting_one_memes import GettingOneMeme
from endpoints.getting_all_memes import GettingAllMemes
from endpoints.verification_token import ExaminationToken


@pytest.fixture()
def get_token_endpoint():
    return GetToken()


@pytest.fixture()
def exam_token_endpoint():
    return ExaminationToken()


@pytest.fixture()
def get_all_memes_endpoint():
    return GettingAllMemes()


@pytest.fixture()
def get_one_meme_endpoint():
    return GettingOneMeme()


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture()
def update_token(get_token_endpoint, exam_token_endpoint):
    """Фикстура для проверки и обновления токена перед выполнением теста"""
    # Проверка существующего токена
    if Endpoint.headers.get("Authorization"):
        # Создаем экземпляр ExaminationToken для проверки токена
        exam_instance = exam_token_endpoint

        # Проверяем валидность текущего токена
        is_valid = exam_instance.examination_token()

        if is_valid:
            print(f"Токен валиден: {Endpoint.headers['Authorization']}")
            return  # Токен валиден, выходим из фикстуры

    # Если токен не существует или не валиден, получаем новый токен
    print("Токен отсутствует или не валиден. Получаем новый токен...")
    token = get_token_endpoint.get_new_token()

    # Обновляем токен в заголовках класса Endpoint
    Endpoint.token = token
    Endpoint.headers['Authorization'] = token

    print(f"Токен обновлен в заголовках: {Endpoint.headers['Authorization']}")


@pytest.fixture()
def cleanup_meme_fixture(request):
    """Фикстура для удаления продукта после выполнения теста"""
    yield
    meme_id = request.function.meme_id
    delete_meme = DeleteMeme()
    delete_meme.delete_meme(created_meme_id=meme_id)


@pytest.fixture()
def create_meme_fixture(create_meme_endpoint):
    """Фикстура для создания мема"""
    created_meme_id = create_meme_endpoint.create_new_meme()
    yield created_meme_id


@pytest.fixture
def remove_token_from_headers():
    """Фикстура для удаления токена из заголовка"""

    endpoint = Endpoint

    endpoint.headers.pop('Authorization', None)
    return endpoint


@pytest.fixture
def create_invalid_token(create_meme_endpoint):
    """Фикстура для подстановки несуществующего токена в заголовки"""
    # Генерация случайного токена длиной 10 символов
    random_token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Устанавливаем сгенерированый токен
    create_meme_endpoint.headers['Authorization'] = random_token
    return create_meme_endpoint


@pytest.fixture()
def get_meme_id_of_another_user(get_all_memes_endpoint):
    """Фикстура для получения meme_id, созданного другим пользователем"""
    # Создаем объект класса
    getting_memes = GettingAllMemes()

    # Получаем все мемы
    getting_memes.getting_all_memes()

    # Получаем случайный id, который не имеет KhalimulinDD в updated_by
    random_meme_id = getting_memes.get_random_stranger_meme_id()

    return random_meme_id


@pytest.fixture()
def getting_your_meme_id(get_all_memes_endpoint):
    """Фикстура для получения meme_id, созданного носителем токена из заголовка"""
    # Создаем объект класса
    getting_memes = GettingAllMemes()

    # Получаем все мемы
    getting_memes.getting_all_memes()

    # Получаем случайный id, который имеет KhalimulinDD в updated_by
    random_meme_id = getting_memes.get_random_meme_id()

    return random_meme_id
