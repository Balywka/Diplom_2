import pytest
import requests
from urls import REGISTER_URL, LOGIN_URL, USER_URL, INGREDIENTS_URL
from generators import generate_email, generate_password, generate_name
from data import EXISTING_USER_BASE

class UserContext:
    #Объект с данными пользователя + методы для работы с ним
    def __init__(self, email, password, name, token):
        self.email = email
        self.password = password
        self.name = name
        self.token = token

    def auth_headers(self):
        #Возвращает заголовки для авторизованных запросов
        return {"Authorization": self.token}

    def delete_self(self):
        #Удаляет пользователя после теста.
        requests.delete(USER_URL, headers=self.auth_headers())


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
    assert reg_resp.status_code == 200, f"Регистрация упала: {reg_resp.text}"
    # получение токена
    login_resp = requests.post(LOGIN_URL, json={"email": email, "password": password})
    assert login_resp.status_code == 200, f"Логин упал: {login_resp.text}"
    token = login_resp.json()["accessToken"]
    user = UserContext(email, password, name, token)
    yield user
    user.delete_self()  # автоматическая очистка


@pytest.fixture(scope="session")
def logged_in_user():
    #Создаёт пользователя ОДИН РАЗ за сессию (например, для тестов "повторная регистрация").
    #Email: test-data+1@yandex.ru
    # Генерируем email
    email = f"test-data+{generate_name().split('#')[-1]}@yandex.ru"
    payload = {**EXISTING_USER_BASE, "email": email}
    # зарегистрировать (если 403 — значит, уже есть — ок)
    reg = requests.post(REGISTER_URL, json=payload)
    assert reg.status_code in (200, 403), f"Не удалось создать пользователя: {reg.text}"
    # Логинимся
    login = requests.post(LOGIN_URL, json=payload)
    assert login.status_code == 200, f"Логин упал: {login.text}"
    data = login.json()
    return {
        "email": data["user"]["email"],
        "name": data["user"]["name"],
        "access_token": data["accessToken"],
        "refresh_token": data["refreshToken"]
    }


@pytest.fixture(scope="session")
def ingredient_ids():
    #Получает 15 ID ингредиентов один раз за сессию.
    #Используется в тестах заказов.
    resp = requests.get(INGREDIENTS_URL)
    assert resp.status_code == 200, "Не удалось получить ингредиенты"
    return [item["_id"] for item in resp.json()["data"]]