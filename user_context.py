import requests
from urls import USER_URL


class UserContext: # Объект с данными пользователя + методы для работы с ним

    def __init__(self, email, password, name, token):
        self.email = email
        self.password = password
        self.name = name
        self.token = token

    def auth_headers(self): # Возвращает заголовки для авторизованных запросов
        return {"Authorization": self.token}

    def delete_self(self):  # Удаляет пользователя после теста
        requests.delete(USER_URL, headers=self.auth_headers())