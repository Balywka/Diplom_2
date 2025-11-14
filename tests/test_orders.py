import requests
import allure
from urls import ORDERS_URL

@allure.feature("Создание заказов")
class TestOrders:

    @allure.title("Создать заказ: авторизован + ингредиенты (200 + номер)")
    def test_create_order_auth_valid(self, registered_user, ingredient_ids):
        payload = {"ingredients": ingredient_ids[:2]}  # 2 первых ингредиента
        resp = requests.post(
            ORDERS_URL,
            json=payload,
            headers=registered_user.auth_headers()  # авторизация
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "order" in data
        assert "number" in data["order"]
        assert isinstance(data["order"]["number"], int)
        assert data["order"]["number"] > 0

    @allure.title("Создать заказ: без авторизации (200 + номер) — разрешено на стенде")
    def test_create_order_no_auth(self, ingredient_ids):
        # Нет заголовков анонимный запрос
        payload = {"ingredients": ingredient_ids[:1]}
        resp = requests.post(ORDERS_URL, json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "order" in data
        assert "number" in data["order"]
        assert isinstance(data["order"]["number"], int)
        assert data["order"]["number"] > 0

    @allure.title("Создать заказ: без ингредиентов (400)")
    def test_create_order_empty_ingredients(self, registered_user):
        resp = requests.post(
            ORDERS_URL,
            json={"ingredients": []},
            headers=registered_user.auth_headers()
        )
        assert resp.status_code == 400
        assert resp.json()["success"] is False
        assert "Ingredient ids must be provided" in resp.json()["message"]

    @allure.title("Создать заказ: невалидный ID ингредиента (500)")
    def test_create_order_invalid_ingredient(self, registered_user):
        payload = {"ingredients": ["invalid_id_xyz"]}
        resp = requests.post(
            ORDERS_URL,
            json=payload,
            headers=registered_user.auth_headers()
        )
        assert resp.status_code == 500  # "невалидный хеш → 500"