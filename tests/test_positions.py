import pytest
from fastapi.encoders import jsonable_encoder

from src.positions.models import Position
from tests.conftest import client, TestingSessionLocal


def test_create_position(position_data1):
    response = client.post('/positions/', json={**position_data1})

    # Case 1: Создание должности, проверка кода ответа, проверка тела ответа
    assert response.status_code == 200, 'Неверный код ответа при создании объекта'
    data = response.json()
    assert data['title'] == position_data1['title'], 'В ответе неверный title'
    assert 'id' in data, 'В ответе не создался id'
    position_id = data['id']

    # Case 2: Создание должности, проверка данных в БД
    with TestingSessionLocal() as db:
        db_position = db.get(Position, position_id)
    assert db_position.title == position_data1['title'], 'В БД записались неверные данные'

    # Case 3: Создание должности с дублем title, проверка кода ответа
    response = client.post('/positions/', json={**position_data1})
    assert response.status_code == 400, 'Неверный код ответа при создании дубля объекта'


def test_get_all_positions(position_data1, position_data2):
    client.post('/positions/', json={**position_data2})
    response = client.get('/positions/')
    # Case 1: Запрос всех должностей, проверка кода ответа
    assert response.status_code == 200, 'Неверный код ответа при получении всего списока объектов'

    # Case 2: Запрос всех должностей, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_positions = db.query(Position).all()
    assert response.json() == jsonable_encoder(db_positions), 'Данные в ответе не совпадают с данными в БД'

    # Case 3: Запрос всех должностей, проверка limit и offset
    response = client.get('/positions/?skip=1&limit=1')
    with TestingSessionLocal() as db:
        db_positions = db.query(Position).offset(1).limit(1).all()
    assert response.json() == jsonable_encoder(db_positions), ('Данные в ответе не совпадают с данными в БД '
                                                               'при использовании offset и limit')


def test_get_position_by_id(position_data1):
    # Case 1: Запрос несуществующей должности, проверка кода ответа
    response = client.get(f'/positions/10000')
    assert response.status_code == 404, 'Неверный код ответа при запросе несуществующего объекта'

    # Case 2: Запрос существующей должности, проверка кода ответа
    with TestingSessionLocal() as db:
        db_positions = db.query(Position).where(Position.title == position_data1["title"]).first()
        position_id = db_positions.id
    response = client.get(f'/positions/{position_id}')
    assert response.status_code == 200, 'Неверный код ответа при запросе существующего объекта'

    # Case 3: Запрос существующей должности, проверка совпадения тела ответа и данных в БД
    assert response.json() == jsonable_encoder(db_positions), 'Данные в ответе не совпадают с данными в БД'


def test_update_position_by_id(position_data1):
    # Case 1: Обновление несуществующей должности, проверка кода ответа
    response = client.put('/positions/10000', json={**position_data1})
    assert response.status_code == 404, 'Неверный код ответа при запросе несуществующего объекта'

    # Case 2: Обновление существующей должности, проверка кода ответа
    with TestingSessionLocal() as db:
        db_positions = db.query(Position).where(Position.title == position_data1["title"]).first()
        position_id = db_positions.id
    position_data1['title'] += ' update'
    response = client.put(f'/positions/{position_id}', json={**position_data1})
    assert response.status_code == 200, 'Неверный код ответа при запросе существующего объекта'

    # Case 3: Обновление существующей должности, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_positions = db.get(Position, position_id)
    assert response.json() == jsonable_encoder(db_positions), 'Данные в ответе и БД не совпадают'

    # Case 4: Обновление существующей должности, проверка тела ответа
    position_data1['id'] = position_id
    assert response.json() == {**position_data1}, 'Данные в ответе неверные'


def test_partial_update_position_by_id(position_data2):
    # Case 1: Обновление несуществующей должности, проверка кода ответа
    response = client.patch('/positions/10000', json={**position_data2})
    assert response.status_code == 404, 'Неверный код ответа при запросе несуществующего объекта'

    # Case 2: Обновление существующей должности, проверка кода ответа
    with TestingSessionLocal() as db:
        db_positions = db.query(Position).where(Position.title == position_data2["title"]).first()
        position_id = db_positions.id
    position_data2['title'] += ' partial update'
    response = client.patch(f'/positions/{position_id}', json={**position_data2})
    assert response.status_code == 200, 'Неверный код ответа при запросе существующего объекта'

    # Case 3: Обновление несуществующей должности, проверка тела ответа
    data = response.json()
    assert data['title'] == position_data2['title'], 'Неверные данные в ответе'

    # Case 4: Обновление несуществующей должности, проверка данных в БД
    with TestingSessionLocal() as db:
        db_positions = db.get(Position, position_id)
    assert db_positions.title == position_data2['title'], 'Неверные данные в БД'


def test_delete_position_by_id(position_data2):
    # Case 1: Удаление несуществующей должности, проверка кода ответа
    response = client.delete('/positions/10000')
    assert response.status_code == 404, 'Неверный код ответа при запросе несуществующего объекта'

    # Case 2: Удаление существующей должности, проверка кода ответа
    with TestingSessionLocal() as db:
        db_positions = db.query(Position).first()
        position_id = db_positions.id
    response = client.delete(f'/positions/{position_id}')
    assert response.status_code == 200, 'Неверный код ответа при запросе существующего объекта'

    # Case 3: Удаление существующей должности, проверка тела ответа
    data = response.json()
    assert data['title'] == db_positions.title, 'Неверные данные в ответе'

    # Case 4: Удаление существующей должности, проверка отсутствия данных в ДБ
    with (TestingSessionLocal() as db):
        is_exist = db.query(Position.id).where(Position.title == data['title']).first() is not None
    assert not is_exist, 'Объект не удален из БД'
