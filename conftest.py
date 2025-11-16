import pytest
import requests
import logging
from urls import REGISTER_URL, LOGIN_URL, USER_URL, INGREDIENTS_URL
from generators import generate_email, generate_password, generate_name
from data import EXISTING_USER_BASE
from user_context import UserContext

logger = logging.getLogger(__name__)

@pytest.fixture()
def registered_user():
    #Создаёт временного пользователя, отдаёт UserContext, удаляет после теста.
    #Используется в 90% тестов.
    email = generate_email()
    password = generate_password()
    name = generate_name()
    payload = {"email": email, "password": password, "name": name}
    # Регистрация
    reg_resp = requests.post(REGISTER_URL, json=payload)
    if reg_resp.status_code != 200:
        pytest.fail(f"Регистрация упала: {reg_resp.text}")
    # получение токена
    login_resp = requests.post(LOGIN_URL, json={"email": email, "password": password})
    if login_resp.status_code != 200:
        pytest.fail(f"Логин упал: {login_resp.text}")
    token = login_resp.json()["accessToken"]
    user = UserContext(email, password, name, token)
    yield user
    # Автоматическая очистка
    try:
        user.delete_self()
    except Exception as e:
        logger.error(f"Ошибка при удалении пользователя: {e}")


@pytest.fixture(scope="session")
def logged_in_user():
    # Создаёт пользователя ОДИН РАЗ за сессию
    email = f"test-data+{generate_name().split('#')[-1]}@yandex.ru"
    payload = {**EXISTING_USER_BASE, "email": email}
    # Регистрация (если 403 — значит, уже есть — ок)
    reg = requests.post(REGISTER_URL, json=payload)
    if reg.status_code not in (200, 403):
        pytest.fail(f"Не удалось создать пользователя: {reg.text}")
    # Логинимся
    login = requests.post(LOGIN_URL, json=payload)
    if login.status_code != 200:
        pytest.fail(f"Логин упал: {login.text}")
    data = login.json()
    return {
        "email": data["user"]["email"],
        "name": data["user"]["name"],
        "access_token": data["accessToken"],
        "refresh_token": data["refreshToken"]
    }


@pytest.fixture(scope="session")
def ingredient_ids():
    # Получает 15 ID ингредиентов один раз за сессию.
    # Используется в тестах заказов.
    resp = requests.get(INGREDIENTS_URL)
    if resp.status_code != 200:
        pytest.fail("Не удалось получить ингредиенты")
    return [item["_id"] for item in resp.json()["data"]]