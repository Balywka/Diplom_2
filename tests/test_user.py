import requests
import allure
from urls import USER_URL
from data import RESP_NOT_AUTHORISED, RESP_EMAIL_EXISTS

@allure.feature("Профиль пользователя")
class TestUser:

    @allure.title("Получить данные: авторизован (200)")
    def test_get_user_data(self, registered_user):
        resp = requests.get(USER_URL, headers=registered_user.auth_headers())
        assert resp.status_code == 200
        assert resp.json()["user"]["email"] == registered_user.email

    @allure.title("Получить данные: без авторизации (401)")
    def test_get_user_no_auth(self):
        resp = requests.get(USER_URL)
        assert resp.status_code == 401
        assert resp.json() == RESP_NOT_AUTHORISED

    @allure.title("Изменить имя: авторизован (200)")
    def test_change_name(self, registered_user):
        new_name = f"Changed #{registered_user.name.split('#')[-1]}"
        resp = requests.patch(USER_URL, json={"name": new_name}, headers=registered_user.auth_headers())
        assert resp.status_code == 200
        assert resp.json()["user"]["name"] == new_name

    @allure.title("Изменить email на занятый (403)")
    def test_change_email_to_existing(self, registered_user):
        resp = requests.patch(USER_URL, json={"email": "test-data@yandex.ru"}, headers=registered_user.auth_headers())
        assert resp.status_code == 403
        assert resp.json() == RESP_EMAIL_EXISTS

    @allure.title("Удалить пользователя (202)")
    def test_delete_user(self, registered_user):
        resp = requests.delete(USER_URL, headers=registered_user.auth_headers())
        assert resp.status_code == 202  # ← именно 202 на стенде