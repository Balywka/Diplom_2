import requests
import allure
from urls import REGISTER_URL, LOGIN_URL
from data import (EXISTING_USER_BASE, RESP_USER_EXISTS, RESP_MISSING_FIELDS, RESP_WRONG_CREDENTIALS)

@allure.feature("Регистрация и вход")
class TestAuth:

    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self, registered_user):
        # registered_user — уже создан и залогинен
        assert registered_user.email.startswith("user_")

    @allure.title("Регистрация существующего пользователя (403)")
    def test_register_existing_user(self, logged_in_user):
        # Пытаемся зарегистрировать того же пользователя ещё раз
        payload = {
            "email": logged_in_user["email"],
            "password": EXISTING_USER_BASE["password"],
            "name": EXISTING_USER_BASE["name"]
        }
        resp = requests.post(REGISTER_URL, json=payload)
        assert resp.status_code == 403
        assert resp.json() == RESP_USER_EXISTS

    @allure.title("Регистрация без email (403)")
    def test_register_missing_email(self):
        payload = {"password": "123", "name": "NoEmail"}
        resp = requests.post(REGISTER_URL, json=payload)
        assert resp.status_code == 403
        assert resp.json() == RESP_MISSING_FIELDS

    @allure.title("Регистрация без password (403)")
    def test_register_missing_password(self):
        payload = {"email": "no@pass.com", "name": "NoPass"}
        resp = requests.post(REGISTER_URL, json=payload)
        assert resp.status_code == 403
        assert resp.json() == RESP_MISSING_FIELDS

    @allure.title("Регистрация без name (403)")
    def test_register_missing_name(self):
        payload = {"email": "no@name.com", "password": "123"}
        resp = requests.post(REGISTER_URL, json=payload)
        assert resp.status_code == 403
        assert resp.json() == RESP_MISSING_FIELDS

    @allure.title("Успешный вход (200)")
    def test_login_success(self, logged_in_user):
        # logged_in_user — уже залогинен в фикстуре
        assert "access_token" in logged_in_user

    @allure.title("Вход с неверным паролем (401)")
    def test_login_wrong_password(self, logged_in_user):
        payload = {
            "email": logged_in_user["email"],
            "password": "wrong_password"
        }
        resp = requests.post(LOGIN_URL, json=payload)
        assert resp.status_code == 401
        assert resp.json() == RESP_WRONG_CREDENTIALS