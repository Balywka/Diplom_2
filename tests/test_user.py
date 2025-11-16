import requests
import allure
from urls import USER_URL
from data import RESP_NOT_AUTHORISED, RESP_EMAIL_EXISTS


@allure.feature("Профиль пользователя")
class TestUser:

    @allure.title("Получить данные: авторизован (200)")
    def test_get_user_data(self, registered_user):
        with allure.step("Запросить данные пользователя"):
            resp = requests.get(USER_URL, headers=registered_user.auth_headers())

        with allure.step("Проверить успешное получение данных"):
            assert resp.status_code == 200
            assert resp.json()["user"]["email"] == registered_user.email

    @allure.title("Получить данные: без авторизации (401)")
    def test_get_user_no_auth(self):
        with allure.step("Запросить данные без авторизации"):
            resp = requests.get(USER_URL)

        with allure.step("Проверить ошибку авторизации"):
            assert resp.status_code == 401
            assert resp.json() == RESP_NOT_AUTHORISED

    @allure.title("Изменить имя: авторизован (200)")
    def test_change_name(self, registered_user):
        new_name = f"Changed #{registered_user.name.split('#')[-1]}"

        with allure.step("Изменить имя пользователя"):
            resp = requests.patch(USER_URL, json={"name": new_name},
                                  headers=registered_user.auth_headers())

        with allure.step("Проверить успешное изменение имени"):
            assert resp.status_code == 200
            assert resp.json()["user"]["name"] == new_name

    @allure.title("Изменить email на занятый (403)")
    def test_change_email_to_existing(self, registered_user):
        with allure.step("Попытаться изменить email на занятый"):
            resp = requests.patch(USER_URL, json={"email": "test-data@yandex.ru"},
                                  headers=registered_user.auth_headers())

        with allure.step("Проверить ошибку существующего email"):
            assert resp.status_code == 403
            assert resp.json() == RESP_EMAIL_EXISTS

    @allure.title("Удалить пользователя (202)")
    def test_delete_user(self, registered_user):
        with allure.step("Удалить пользователя"):
            resp = requests.delete(USER_URL, headers=registered_user.auth_headers())

        with allure.step("Проверить успешное удаление"):
            assert resp.status_code == 202