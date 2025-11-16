import requests
import allure
import pytest
from urls import REGISTER_URL, LOGIN_URL
from data import (EXISTING_USER_BASE, RESP_USER_EXISTS, RESP_MISSING_FIELDS,
                  RESP_WRONG_CREDENTIALS)
from generators import generate_email, generate_password, generate_name
from user_context import UserContext


@allure.feature("Регистрация и вход")
class TestAuth:

    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self):
        # Шаг теста: создание пользователя
        email = generate_email()
        password = generate_password()
        name = generate_name()

        with allure.step("Отправить запрос на регистрацию"):
            payload = {"email": email, "password": password, "name": name}
            resp = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверить успешную регистрацию"):
            assert resp.status_code == 200
            assert resp.json()["success"] is True
            assert resp.json()["user"]["email"] == email
            assert resp.json()["user"]["name"] == name

    @allure.title("Регистрация существующего пользователя (403)")
    def test_register_existing_user(self, logged_in_user):
        with allure.step("Пытаемся зарегистрировать того же пользователя ещё раз"):
            payload = {
                "email": logged_in_user["email"],
                "password": EXISTING_USER_BASE["password"],
                "name": EXISTING_USER_BASE["name"]
            }
            resp = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверить ошибку существующего пользователя"):
            assert resp.status_code == 403
            assert resp.json() == RESP_USER_EXISTS

    @pytest.mark.parametrize("payload,missing_field", [
        ({"password": "123", "name": "NoEmail"}, "email"),
        ({"email": "no@pass.com", "name": "NoPass"}, "password"),
        ({"email": "no@name.com", "password": "123"}, "name")
    ])
    @allure.title("Регистрация без обязательного поля")
    def test_register_missing_field(self, payload, missing_field):
        with allure.step(f"Отправить запрос на регистрацию без поля {missing_field}"):
            resp = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверить ошибку отсутствия обязательных полей"):
            assert resp.status_code == 403
            assert resp.json() == RESP_MISSING_FIELDS

    @allure.title("Успешный вход (200)")
    def test_login_success(self):
        # Шаг теста: создание и авторизация пользователя
        email = generate_email()
        password = generate_password()
        name = generate_name()

        with allure.step("Зарегистрировать пользователя"):
            reg_payload = {"email": email, "password": password, "name": name}
            reg_resp = requests.post(REGISTER_URL, json=reg_payload)
            assert reg_resp.status_code == 200

        with allure.step("Выполнить вход с корректными данными"):
            login_payload = {"email": email, "password": password}
            resp = requests.post(LOGIN_URL, json=login_payload)

        with allure.step("Проверить успешный вход"):
            assert resp.status_code == 200
            assert "accessToken" in resp.json()
            assert resp.json()["user"]["email"] == email
        # Очистка
        try:
            token = resp.json()["accessToken"]
            user = UserContext(email, password, name, token)
            user.delete_self()
        except Exception:
            pass

    @allure.title("Вход с неверным паролем (401)")
    def test_login_wrong_password(self, logged_in_user):
        with allure.step("Выполнить вход с неверным паролем"):
            payload = {
                "email": logged_in_user["email"],
                "password": "wrong_password"
            }
            resp = requests.post(LOGIN_URL, json=payload)
        with allure.step("Проверить ошибку авторизации"):
            assert resp.status_code == 401
            assert resp.json() == RESP_WRONG_CREDENTIALS