import json

from tests.conftest import TestingSessionLocal, client


def test_get_busy_users(load_test_data_in_db):
    # Запрос на всех занятых пользователей вместе с задачами
    # Проверка на подготовленных данных
    with open('tests/service_test_busy_users.json') as json_file:
        data = json.load(json_file)

    response = client.get('/services/busy_users')
    assert data == response.json(), 'Неверная выгрузка'


def test_get_important_tasks(load_test_data_in_db):
    # Запрос на всех важные задачи
    # Проверка на подготовленных данных
    with open('tests/service_test_important_tasks.json') as json_file:
        data = json.load(json_file)

    response = client.get('/services/important_tasks')
    assert data == response.json(), 'Неверная выгрузка'
