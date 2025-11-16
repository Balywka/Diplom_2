
_counter = 0  # счётчик живёт всё время сессии pytest

def _next_id():
    #Возвращает 1, 2, 3 при каждом вызове
    global _counter
    _counter += 1
    return _counter

def generate_email():
    #Генерит уникальный email: user_1@test.ru, user_2@test.ru
    return f"user_{_next_id()}@test.ru"

def generate_password():
    # одинаковый пароль для стабильности
    return "Pass123!"

def generate_name():
    return f"User#{_next_id()}"