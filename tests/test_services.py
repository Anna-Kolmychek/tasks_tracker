import pytest


@pytest.fixture
def load_data_in_db():
    # очистка БД и загрузка данных из db_data.dump
    pass


def test_get_busy_users(load_data_in_db):
    # Запрос на всех занятых пользователей вместе с задачами
    # Проверка на подготовленных данных
    pass


def test_get_important_tasks(load_data_in_db):
    # Запрос на всех важные задачи
    # Проверка на подготовленных данных
    pass

