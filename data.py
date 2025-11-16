# Пользователь для тестов
EXISTING_USER_BASE = {
    "password": "password1",
    "name": "Username"
}

# Ожидаемые ответы
RESP_USER_EXISTS = {"success": False, "message": "User already exists"}
RESP_MISSING_FIELDS = {"success": False, "message": "Email, password and name are required fields"}
RESP_WRONG_CREDENTIALS = {"success": False, "message": "email or password are incorrect"}
RESP_NO_INGREDIENTS = {"success": False, "message": "Ingredient ids must be provided"}
RESP_NOT_AUTHORISED = {"success": False, "message": "You should be authorised"}  # ← ВАЖНО: s, не z!
RESP_EMAIL_EXISTS = {"success": False, "message": "User with such email already exists"}
RESP_LOGOUT_SUCCESS = {"success": True, "message": "Successful logout"}